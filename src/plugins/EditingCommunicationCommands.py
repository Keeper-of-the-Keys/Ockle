#!/usr/bin/env python
"""  Ockle PDU and servers manager
A plugin to add a commands that let you modify Ockle config files. 

Created on May 16, 2012

@author: Guy Sheffer <guy.sheffer at mail.huji.ac.il>
"""
import os.path,sys
p = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','common')
sys.path.insert(0, p)
from plugins.ModuleTemplate import ModuleTemplate
import pygraph.readwrite.dot
import traceback
import shutil,time
from common.common import getINIstringtoDict
from common.common import mergeDicts
from common.common import dictToConfig

import json

class EditingCommunicationCommands(ModuleTemplate):
    ''' Add a commands that let you modify Ockle config files'''
    def __init__(self,MainDaemon):
        ModuleTemplate.__init__(self,MainDaemon)
        return
    
    def _getINIFile(self,path):
        ''' Gets an INI file, returns an empty file if does not exist
        '''
        fileContent =" "
        try:
            path = os.path.join(self.mainDaemon.ETC_DIR,path)
            print path
            
            with open(path, 'r') as content_file:
                fileContent = content_file.read()
        except:
            traceback.print_exc(file=sys.stdout)
        return fileContent
    
    def getINIFileCommand(self,path):
        return {"File" :  self._getINIFile(path)}
    
    def setINIFileCommand(self,dataDict):
        iniDict = json.loads(dataDict["iniDict"])
        return self._setINIFile(dataDict["Path"],iniDict)
    
    def _setINIFile(self,path,iniDict):
        path = os.path.join(self.mainDaemon.ETC_DIR,path)
        
        #create folder if does not exist
        pathDir = os.path.dirname(path)
        if not os.path.isdir(pathDir):
            os.mkdir(pathDir)
        
        iniSource =  getINIstringtoDict(self._getINIFile(path))
        newConfig={}
        
        for section in iniDict.keys():
            if section in iniSource:
                newConfig[section] = mergeDicts(iniSource[section],iniDict[section])
            else:
                newConfig[section] = iniDict[section]
        
        config = dictToConfig(newConfig)
        try:
            #shutil.copy(path,path + "." + str(int(time.time())))
            pass
        except:
            pass
        config.write(open(path,"w"))
        #print newConfig
        return {"succeeded": True}
    
    def deleteINIFileCommand(self,path):
        path = os.path.join(self.mainDaemon.ETC_DIR,path)
        
        #DEBUG for now
        try:
            backPath = os.path.join(self.mainDaemon.ETC_DIR,"serversBack")
            os.system("mkdir -p " +backPath)
            shutil.copy(path,backPath)
        except:
            pass
        
        returnValue = {"succeeded": True}
        
        try:
            os.remove(path)
        except OSError as e:
            returnValue["succeeded"] = False
            returnValue["error"] = str(e)
        return returnValue
    
    def deleteINISectionCommand(self,path,section):
        try:
            iniFileDict = getINIstringtoDict(self._getINIFile(path))
            iniFileDict.pop(section)
            self._setINIFile(path,iniFileDict)
            return {"succeeded" : True}
        except:
            pass
        return {"succeeded" : False,
                "error" : "Failed remove section " + section + " in file " + path}
    
    
    
    def run(self):
        self.debug("\n")
        self.mainDaemon.communicationHandler.AddCommandToList("getINIFile",lambda dataDict: self.getINIFileCommand(dataDict["Path"]))
        self.mainDaemon.communicationHandler.AddCommandToList("setINIFile",lambda dataDict: self.setINIFileCommand(dataDict))
        self.mainDaemon.communicationHandler.AddCommandToList("deleteINIFile",lambda dataDict: self.deleteINIFileCommand(dataDict["Path"]))
        self.mainDaemon.communicationHandler.AddCommandToList("deleteINIFile",lambda dataDict: self.deleteINIFileCommand(dataDict["Path"]))
        self.mainDaemon.communicationHandler.AddCommandToList("deleteINISection",lambda dataDict: self.deleteINISectionCommand(dataDict["Path"],dataDict["Section"]))
        return

if __name__ == "__main__":
    a = EditingCommunicationCommands(None)