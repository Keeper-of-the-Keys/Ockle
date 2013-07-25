#!/usr/bin/env python
""" Common SNMP functions for Ockle

Created on 5773 Av 2/2013 Jul 9.

Based on code formerly in Raritan Dominion PDU plugin, and nagios work for HUJI

@author: E.S. Rosenberg <esr+ocklesource at mail.hebrew.edu>
"""

# GETNEXT Command Generator
from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp

from pysnmp.proto import rfc1902

# GET Command Generator
from pysnmp.entity.rfc3413.oneliner import cmdgen

cmdGen = cmdgen.CommandGenerator()
mibBuilder = cmdGen.snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder

def bool2int(bool):
    if bool:
        return 1
    return 0

def int2bool(int):
    if int == 1:
        return True
    return False

def snmpGetter(snmp_host, snmp_port, authData, *oids):
    '''Simple function that handles all snmp get logic

    Takes:
    snmp_host - hostname, fqdn, ip-address of target host
    snmp_port - port number
    authData - object generated by snmpCreatAuthData()
    *oids - list of one or more OIDs needed.

    This function will raise exceptions on errors!
    '''

    #cmdGen = cmdgen.CommandGenerator()
    global cmdGen

    if ( not isinstance(authData, cmdgen.CommunityData) 
         and not isinstance(authData, cmdgen.UsmUserData) ):
        raise Exception("No authdata provided!")
        

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        authData,
        cmdgen.UdpTransportTarget((snmp_host, snmp_port)),
        *oids,
        lookupNames = True,
        lookupValues = True)

    if errorIndication:
        raise Exception("An Error Occurred: {}".format(errorIndication))
    else:
        if errorStatus:
            raise Exception('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1] or '?')
            )
        else:
            return varBinds
    
    return false

def snmpGetSingle(snmp_host, snmp_port, authData, oid):
    '''Simple wrapper of snmpGetter for single values.

    Since snmpGetter returns an object containing one or more results and a 
    lot of the ockle code may rely on other types of return values.
    '''
    try:
        result = snmpGetter(snmp_host, snmp_port, authData, oid)
    except Exception as e:
        print e
        return False

    for name, val in result:
        return name, val

def snmpSetter(snmp_host, snmp_port, authData, oid_values):
    '''Simple function to handle SNMP SET operations

    Takes:
    snmp_host -  hostname, fqdn, ip-address of target host
    snmp_port - port number
    authData - object generated by snmpCreatAuthData()
    *oid_values - list of oid, value tupples.

    Function raises exceptions.
    '''

    global cmdGen

    if ( not isinstance(authData, cmdgen.CommunityData) 
         and not isinstance(authData, cmdgen.UsmUserData) ):
        raise Exception("No authdata provided!")
    
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
        authData,
        cmdgen.UdpTransportTarget((snmp_host, snmp_port)),
        oid_values
    )

    if errorIndication:
        raise Exception("An Error Occurred: {}".format(errorIndication))
    else:
        if errorStatus:
            raise Exception('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex)-1] or '?')
            )
        else:
            return varBinds
    
    return false

                                                                       

    
def snmpCreateAuthData(snmp_version, snmp_community=''):
    '''Function to generate authData for SNMP calls

    Function doesn't handle SNMPv3 yet!
    Function can throw an exception.
    '''
    if snmp_version == 1:
        authData = cmdgen.CommunityData(snmp_community, 0)
    elif snmp_version == '2c':
        authData = cmdgen.CommunityData(snmp_community)
    elif snmp_version == 3:
        raise Exception("Currently snmpCreateAuthData() does not support SNMPv3")
        # TODO: for future SNMPv3 support:
        # cmdgen.UsmUserData('securityName', 'authkey1', 'privkey1'),
    
    return authData
