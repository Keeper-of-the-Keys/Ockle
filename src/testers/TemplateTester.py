#!/usr/bin/env python
"""  Ockle PDU and servers manager
This is a template module that all other test modules extend

Created on Apr 25, 2012

@author: Guy Sheffer <guy.sheffer at mail.huji.ac.il>
"""

class TesterOpState():
    INIT=-1# Did not start yet
    SUCCEEDED=0
    FAILED=1
    

class TemplateTester(object):
    def __init__(self,testerConfigDict,testerParams):
        self.opState = TesterOpState.INIT
        return
    
    def test(self):
        '''
        Runs the test
        '''
        return
    
    def setOpState(self,state):
        self.opState=state
    def getOpState(self):
        return self.opState