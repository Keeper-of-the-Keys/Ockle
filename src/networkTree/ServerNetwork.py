#!/usr/bin/env python
""" Ockle PDU and servers manager
The server network data structure.
Holds either a DAG of servers with outlets, or a DAG of services (depends how you look at it)

Created on Mar 14, 2012

@author: Guy Sheffer <guy.sheffer at mail.huji.ac.il>
"""
import networkTree.Exceptions as Exceptions
import time

from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write

from outlets.OutletTemplate import OutletOpState
from ServerNode import ServerNodeOpState

from pygraph.algorithms.cycles import find_cycle
from pygraph.algorithms.sorting import topological_sorting
#from pygraph.readwrite.dot import write

class ServerNetwork():
    '''
    The class that handles the graph server network
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.graph = digraph()
        
    def addServer(self,node,dependencies=[]):
        '''Add a server to the network
        
        :param node: a server in the network
        :param dependencies: list of the server names this sever is dependent on
        '''
        self.graph.add_node(node.getName(), node)
        for dep in dependencies:
            self.addDependency(dep,node.getName())
        return
    def addDependency(self,server,dependency):
        ''' Add a dependency to a server
        
        :param server: the name of the server
        :param dependency: the name of the server the former is dependent on  
        :raise DependencyException: Will raise an exception if there was a cycle in the server network
        '''
        self.graph.add_edge(((dependency,server))) #Note this is a turple casting
        cycleCheck = find_cycle(self.graph)
        if len(cycleCheck) != 0:
            raise Exceptions.DependencyException(cycleCheck,"There was a cycle in the server network")
        return
    
    def removeDependency(self,server,dependency):
        ''' Remove a dependency from a server
        
        :param server: the name of the server
        :param dependency: the name of the server the former is dependent on  
        '''
        self.graph.del_edge(((dependency,server))) #Note this is a turple casting
        return
    
    def allOff(self):
        '''Turn all servers off ungracefully
        '''
        nodeList = topological_sorting(self.graph)
        for node in nodeList:
            server = self.graph.node_attributes(node)
            for outlet in server.getOutlets():
                outlet.setState(False)
        return
    
    def initiateStartup(self):
        time.sleep(5)
        nodeList = self.getSortedNodeList()
        for server in nodeList:
            for outlet in server.getOutlets():
                outlet.setState(True)
            time.sleep(1)
        return
    
    def getSortedNodeList(self):
        '''
        returns a list of the nodes topologically sorted
        
        :return: a list of the nodes topologically sorted
        '''
        nodeList = topological_sorting(self.graph)
        servers=[]
        for node in nodeList:
            servers.append(self.graph.node_attributes(node))
        return servers
    
    def getServer(self,serverNameSearch):
        ''' Get a server by name
        
        :param serverNameSearch: The server to search for
        :return: The server class, None if not found
        '''
        for server in self.getSortedNodeList():
            if server.getName() == serverNameSearch:
                return server
        return None
    
    def getSortedNodeListIndex(self):
        ''' returns a list of the node names topologically sorted
        
        :return: a list of the node names topologically sorted
        '''
        return topological_sorting(self.graph)
    
    def getRoot(self):
        ''' Gets the root server of the tree
        
        :return: the root server
        '''
        return self.getSortedNodeList()[0]
    
    
    def isReadyToTurnOn(self,server):
        ''' Is a server ready to be turned on?
        
        :return: True if the server is ready to be turned on '''
        return self.__isReadyAction(server,[ServerNodeOpState.permanentlyFailedToStart],self.getDependencies,ServerNodeOpState.OK)
    
    def __isReadyAction(self,server,autoFalseOpState,relationCallback,opStateRequiredFromParrent):
        ''' Check if a server dependencies are met and tests are met, and could be turned on
        
        :param serverName: the server's name 
        :param autoFalseOpState: OpStates that are automatically considered false
        '''
        serverInstance = self.graph.node_attributes(server)
        if serverInstance.getOpState() in autoFalseOpState:
            return False
        
        parrentServersName = relationCallback(server)
        for parrentServerName in parrentServersName:
            serverNode = self.graph.node_attributes(parrentServerName)
            #failedOutlets = serverNode.getNotOutletsState(OutletOpState.OK)
            if serverNode.getOpState() != opStateRequiredFromParrent:
                return False
            #failedTests = serverNode.getFailedTests()
            #if not self.isReadyToTurnOn(parrentServerName) or failedOutlets or failedTests:
            #    return False
            if not self.__isReadyAction(parrentServerName,autoFalseOpState,relationCallback,opStateRequiredFromParrent):
                return False
        return True
    
    def isReadyToTurnOff(self,server):
        return self.__isReadyAction(server,[ServerNodeOpState.permanentlyFailedToStop],self.getDependent,ServerNodeOpState.OFF)
    
    def getDependencies(self,server):
        '''
        Get a list of servers a given server is dependent on (only one level)
        
        :param server: the server name
        '''
        return self.graph.reverse().neighbors(server)
    
    def getDependent(self,server):
        '''
        Get a list of servers that are dependent on this server
        
        :param server: the server name
        '''
        return self.graph.neighbors(server)
    
    def turningOn(self):
        '''
        
        :return: true if we have any servers that are in intermediate states
        '''
        nodeList = self.getSortedNodeList()
        for server in nodeList:
            if server.getOpState() in [ServerNodeOpState.INIT,ServerNodeOpState.SwitcingOn,ServerNodeOpState.SwitchingOff]:
                return True
        return False
    
    def getServernode(self,serverName):
        ''' Get a server node by name
        
        :param serverName: The name of the server node
        :return: The server node
        '''
        return self.graph.node_attributes(serverName)
        
    def isAllOpState(self,opState):
        ''' Check if all servers are ok
        
        :return: True if all servers are on
        '''
        for server in self.getSortedNodeList():
            if server.getOpState() != opState:
                return False
        return True
    
    def turnOnServer(self,serverName):
        ''' Turn a server on by name
        
        :param serverName: The server name
        '''
        return self.getServer(serverName).turnOn()
    
    def turnOffServer(self,serverName):
        ''' Turn a server off by name
        
        :param serverName: The server name
        '''
        return self.getServer(serverName).turnOff()
    
    def updateNetwork(self):
        ''' Updates the opstate of all the nodes and their outlets/tests and controllers
        '''
        for server in self.getSortedNodeList():
            server.updateOpState()
            
        return
