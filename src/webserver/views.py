#pyramid stuff
from pyramid.renderers import get_renderer
from pyramid.view import view_config
from pyramid.response import Response

#ockle stuff
from ockle_client.ClientCalls import getServerTree
from ockle_client.ClientCalls import getServerView
from ockle_client.DBCalls import getServerStatistics
from common.common import OpState

#graphviz
import pygraphviz as pgv

import time
from datetime import datetime
import json

PLOT_STEP=3600

@view_config(route_name='serverView',renderer="templates/server_info.pt")
def serverPage(request):
    ''' Server View page 
    '''
    def unix2javascript(time):
        ''' Convert a unix timestamp to a javascript timestamp
        @param time: Unix timestamp
        @return: Javascript timestamp
        '''
        return time*1000.0
    
    def javascript2unix(time):
        ''' Convert a javascript timestamp to a unix timestamp
        @param time: Javascript timestamp
        @return: Unix timestamp
        '''
        return time/1000
    
    def getMinMaxListofLists(l,key):
        ''' Get the min and max of a list of lists, takes a list and the key value
        @param l: a list of lists, or list of dicts
        @param key: the key number of the list
        @return: tuple of the min and max values
        '''
        try:
            Min = l[0][key]
            Max = l[0][key]
        except KeyError:
            return 0 
        for element in l:
            if Max < element[key]:
                Max = element[key]
            if Min > element[key]:
                Min =  element[key]
        return Min,Max
    
    serverName = request.matchdict['serverName'];
    
    serverDict = getServerView(serverName)
    if type(serverDict) == dict:
        

        for key in serverDict.iterkeys():
            try:
                serverDict[key] = serverDict[key][0]
            except:
                pass
        
        serverDict["Switch"]=""
        if serverDict["OpState"] ==  str(OpState.OK) or serverDict["OpState"] == str(OpState.SwitchingOff):
            serverDict["Switch"]="on"
        else:
            print serverDict["OpState"]
            serverDict["Switch"]="off"
    else:
        serverDict={}
        serverDict["Switch"]="off"
        
    dataLog=[]
    serverLog = getServerStatistics(serverName,time.time() - 60*60*3,time.time()+1)
    
    for key in serverLog.keys():
        dataDict = json.loads(serverLog[key]["dataDict"])
        dataPointTime=serverLog[key]["time"]
        
        dataPoint=0 #init before assignment
        if dataDict.has_key("outlet1"):
            if dataDict["outlet1"].has_key("CPU"):
                dataPoint=dataDict["outlet1"]["CPU"]
        #dataPoint=serverLog[key]["time"]
        #print "yay"
        #dataLog.append([datetime.fromtimestamp(float(dataPointTime)).strftime('%H:%M:%S'),float(dataPoint)])
        dataLog.append([unix2javascript(float(dataPointTime)),float(dataPoint)])
    minTime,maxTime = getMinMaxListofLists(dataLog,0)
    
    minTime=  javascript2unix(minTime)
    maxTime = javascript2unix(maxTime)
    ticks=[]
    for timestamp in range(int(minTime),int(maxTime),PLOT_STEP):
        ticks.append([datetime.fromtimestamp(timestamp).strftime("%H:%M")])
    return {"layout": site_layout(),
            "xdottree" : "",
            "server_dict" : serverDict,
            "page_title" : "Server View: " + str(serverName),
            "ServerLog" : str(serverLog),
            "dataLog" : str(dataLog),
            "ticks" : str(ticks)}
    #return Response(str(getServerView(request.matchdict['serverName'])))

def site_layout():
    renderer = get_renderer("templates/global_layout.pt")
    layout = renderer.implementation().macros['layout']
    return layout

@view_config(renderer="templates/index.pt")
def index_view(request):
    '''
    View of the server network
    '''
    dot= getServerTree()
    
    gv = pgv.AGraph(string=dot,weights=False)
    #TODO: fix this ugly escape character, ie add a javascript variable wrapper
    #gv.node_attr.update(href="javascript:void(click_node(\\'\\\N\\'))")
    gv.node_attr.update(href="server/\\\N")
    gv.node_attr.update(title="server/\\\N")
    gv.node_attr.update(style="filled")
    gv.node_attr.update(fillcolor="#dbdbdb")
    gv.node_attr.update(name="bla")
    
    for node in gv.nodes():
        print node.get_name()
    
    gv.layout(prog='dot')
    
    return {"layout": site_layout(),
            "page_title": "Server Network View",
            "xdottree" : gv.draw(format="xdot").replace('\n','\\n\\\n')}


@view_config(renderer="templates/about.pt", name="about.html")
def about_view(request):
    return {"layout": site_layout(),
            "page_title": "About"}

# Dummy data
COMPANY = "ACME, Inc."

PEOPLE = [
        {'name': 'sstanton', 'title': 'Susan Stanton'},
        {'name': 'bbarker', 'title': 'Bob Barker'},
]

PROJECTS = [
        {'name': 'sillyslogans', 'title': 'Silly Slogans'},
        {'name': 'meaninglessmissions', 'title': 'Meaningless Missions'},
]
