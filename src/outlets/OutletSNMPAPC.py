#!/usr/bin/env python
'''APC Rack PDU plugin for Ockle

Created on Jul 18, 2013

@author: E.S. Rosenberg <esr+ocklesource at mail.hebrew.edu>
'''

from common.snmp import *

from OutletTemplate import OutletTemplate
class APC_Rack_PDU(OutletTemplate):
    '''APC Rack PDU
    
    Some relevant/used OIDs:
        sPDUOutletCtl - 1.3.6.1.4.1.318.1.1.4.4.2.1.3.{outlet}
            Allows one to set the state of an outlet
        rPDUOutletStatusLoad - 1.3.6.1.4.1.318.1.1.12.3.5.1.1.7.{outlet}
            Should allow one to read the load on a particular outlet,
            currently our PDU is connected to a single instead of a three phase
            feeder which causes it not to sense load.
            (or it is actually malfunctioning)
    '''

    def __init__(self,name,outletConfigDict,outletParams):
        print outletConfigDict,outletParams
        
        self.hostname = outletConfigDict['pdu']['hostname']
        self.snmp_port = int(outletConfigDict['pdu']['snmp_port'])
        self.snmp_version = outletConfigDict['pdu']['snmp_version']
        self.outletNumber = int(outletParams['socket'])
        self.ReadCommunity = outletConfigDict['pdu']["read_community"]
        self.WriteCommunity = outletConfigDict['pdu']["write_community"]

        OutletTemplate.__init__(self,name,outletConfigDict,outletParams)
        self.updateState()

        self.updateData()

        return

    def _setOutletState(self, state):
        '''Sets outlet on or off
        
        APC PDU over SNMP has the following states:
        1 - on
        2 - off
        3 - reboot
        5 - on with delay
        6 - off with delay
        7 - reboot with delay
        
        This function only uses 1 and 2, others may be supported later.
        
        OID[sPDUOutletCtl]: 1.3.6.1.4.1.318.1.1.4.4.2.1.3.{outlet}
        '''
        
        if state:
            state = rfc1902.Integer(1)
        elif not state:
            state = rfc1902.Integer(2)

        try:
            snmpSetter(self.hostname, self.snmp_port, 
                            snmpCreateAuthData(self.snmp_version, 
                                               self.WriteCommunity), 
                       ('1.3.6.1.4.1.318.1.1.4.4.2.1.3.{}'.format(
                           self.outletNumber), state))
        except Exception as e:
            print e

        return

    def _getOutletState(self):
        '''Currently only handles On/Off state and none of the other states
        '''
        try:
            name, val = snmpGetSingle(self.hostname, self.snmp_port,
                                      snmpCreateAuthData(self.snmp_version,
                                                         self.ReadCommunity),
                                      '1.3.6.1.4.1.318.1.1.4.4.2.1.3.{}'.format(
                                          self.outletNumber))
        except Exception as e:
            val = 2
            print e

        if val == 1:
            return True
        elif val == 2:
            return False

        return False

    def updateData(self):
        try:
            oid = '1.3.6.1.4.1.318.1.1.12.3.5.1.1.7.{}'.format(self.outletNumber)
            self.data["current"] = int(snmpGetSingle(self.hostname, 
                                                     self.snmp_port,
                                                     snmpCreateAuthData(
                                                         self.snmp_version,
                                                         self.ReadCommunity),
                                                     oid)[1])
        except Exception as e:
            self.data["current"] = 0
            print e

        return self.data

    def haveFun(self, interval):
        '''Function to turn all outlets on and off sequentially
        '''
        state = 1
        import time
        while 1 == 1:
            for outlet in range(1,25):
                try:
                    snmpSetter(self.hostame, self.snmp_port, snmpCreateAuthData(
                        self.snmp_version, snmp.WriteCommunity), 
                    ('1.3.6.1.4.1.318.1.1.4.4.2.1.3.{}'.format(outlet), 
                     rfc1902.Integer(state)))
                except Exception as e:
                    print e
                    time.sleep(interval)
                    if state == 1:
                        state = 2
                    elif state == 2:
                        state = 1
