#!/usr/bin/env python
'''APC Rack PDU plugin for Ockle

Created on Jul 18, 2013

@author: E.S. Rosenberg <esr+ocklesource at mail.hebrew.edu>
'''

from common.snmp import *

from OutletTemplate import OutletTemplate
class APC_Rack_PDU(OutletTemplate):
    '''APC Rack PDU
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
            oid = '1.3.6.1.4.1.318.1.1.4.4.2.1.3.{}'.format(self.outletNumber)
            self.data["current"] = int(snmpGetSingle(self.hostname, 
                                                     self.snmp_port,
                                                     snmpCreateAuthData(
                                                         self.snmp_version,
                                                         self.ReadCommunity),
                                                     oid))
        except Exception as e:
            self.data["current"] = 0
            print e

        return self.data
