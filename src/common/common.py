#!/usr/bin/env python
""" Ockle PDU and servers manager
Common functions for the whole project
Moved here to avoid code repetition

Created on May 10, 2012

@author: Guy Sheffer <guy.sheffer at mail.huji.ac.il>
"""
from ConfigParser import SafeConfigParser
import os.path, sys
import json

class OpState:
    '''
    Operation state enum, that all other operation states enums extend
    '''
    OK=0
    failedToStart=1
    failedToStop=2
    SwitcingOn = 3
    SwitchingOff = 4
    
COLOR_DICT={
            -1:"black",
            OpState.OK:"green",
           OpState.failedToStart:"red",
           OpState.failedToStop:"yellow",
           OpState.SwitcingOn:"grey",
           OpState.SwitchingOff:"blue",
           }
    

def loadConfig():
    ''' Get the config file and folder
    @return: a tuple with a config parser to config.ini and the etc folder'''
    config = SafeConfigParser()
    ETC_DIR= appendProjectPath("etc")
    config.read(os.path.join(ETC_DIR,"config.ini"))
    return config,ETC_DIR

def appendProjectPath(path):
    ''' Appends the project path to a relative path
    @param path: the internal path
    @return: the relative path 
    '''
    return os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])),path)

def turpleList2Dict(tupleList):
    ''' Convert a tuple list to a dict. For easy and saner access
    Used in this project because config parser returns a list of tuples
    @param tupleList the list of tuples
    @return: a dict with lists for each variable
    '''
    returnDict={}
    for turple in tupleList:
        key = turple[0]
        data = turple[1]
        if data.startswith("["):#turn to a list if lists
            data = json.loads(data)
        returnDict[key]=data
    return returnDict