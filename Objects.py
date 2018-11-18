from PyQt5.QtWidgets import * #GUI (Graphical User Interface) library
from PyQt5 import QtGui, QtCore

import Nodes
import Graphics
#@todo have edges w configurable behavior (packet filters in gns3)
class Network(object):#@todo able to save snapshot of page layout, make master controller which coordinates global stuff - nodes only know themselves and their terminals/edges, network knows bigger picture stuff
    #@todo have dict connecting each baseobj to its graphicsobj if not headless - network is interface
    def __init__(self,initialState=None,nodes=None):
        if initialState is not None:
            self.loadNet(initialState)
        else:
            self.nodes=dict()
            self.edges=dict()
        self.availableNodes=nodes
#        for i in 
    def createNode(self,nodetype='Node',label=None,defloc=None,color='red'):
        if label is None:
            label=len(self.nodes)+1
#        print(label)
        self.nodes[label]=getattr(Nodes,nodetype)(name=label)
#        print (self.nodes[label])
        return self.nodes[label]
    def saveNet(self):
        pass
    def loadNet(self):
        pass
    def connectNodes(self,nfrom=1,nto=2):
        
        FROMNODE=self.nodes[nfrom]
        TONODE=self.nodes[nto]
        
        nd={'from':FROMNODE,'to':TONODE}
        ntpl=(nfrom,nto) #nd can't be used as a key for another dict
#        xto,yto=senarr=ndlf.nodes[nto].gnode.pos()
#        xfrom,yfrom=self.nodes[nfrom].gnode.pos()
        #@todo clean up this code
        if ntpl in self.edges.keys():#checks if refers right
#        
            self.edges[ntpl].updatePos()
#            self.scene.removeItem(self.edges[narr])
            edge=self.edges[ntpl]
        else:#@todo clean up this fn
            edgeobj=Edge(FROMNODE,TONODE)#refers to actual Objects object, while next line is graphics
            edge=Graphics.arrowEdge(FROMNODE.gnode.x()+FROMNODE.sz['x'],FROMNODE.gnode.y()+FROMNODE.sz['y'],TONODE.gnode.x()+FROMNODE.sz['x'],TONODE.gnode.y()+FROMNODE.sz['y'],nodedict=nd,edgeobj=edgeobj)
#        print(ntpl)
        self.edges[ntpl]=edge
    
        FROMNODE.edges[nto]=edge
        TONODE.edges[nfrom]=edge
        return edge
    
    def breakConnect(self,nfrom,nto):
        pass
    def forceModel(self,typ):    #do stuff like spring models here

        pass
    def isDirected(self):
        pass
    def toggleShowDirected(self):
        pass #saves directed data just mirrors matrix & keeps mags const 
        
    def transpose(self):
        pass
    
    def generateAdjMat(self,root=0):
        n=len(self.nodes)
        A=np.zeros((n,n))
        for i in self.edges.keys():
            ii=(i[0]-1,i[1]-1)
            A[ii]=1
            if self.undir:
                A[ii[1],ii[0]]=1
        return A
            
#   
#    CURRENTLY INACTIVE - delete if possible
#class Node(object):#baseclass for nodes - "dumb" & doesn't know who is connected to/[what type of edge (maybe bad idea?)], that's edges job
#    #@todo define trigger here?
#    def __str__(self):
#        return str(self.__class__.__name__)+' '+str(self.name) #makes able to refer to node as "{Nodetype} {integer (unless name is otherwise changed)}" - ie "PrintNode 3" "PrintNode 5" "InputNode 9" ...- useful for debugging 
#    def __init__(self,name,sz={'x':50,'y':50},nterm=10,slotless=False,fn=None,widget=None,graphic=None):
##        self.slots=dict()
#        self.widget=widget
#        self.nterm=nterm
#        self.graphics={'graphicobj':'graphicNode',
#                       'btnlabel':''}
##        self.qt=QGraphicsRectItem
#        self.name=name
#        self.graphic=graphic
#        self.sz=sz
#        self.edges=dict()
#        self.terminals=dict({'in':dict(),'out':dict()})#@todo make this the way to decide direction from node?b 
#        defaultfn=lambda x:x#output is input
#        if fn is not None:
#            self.fn=fn
#        else:
#            self.fn=defaultfn
#    def nodeReady(self,*a,**kw):
#        print(kw)
#    def preprocess(self,values=None):
#        pass
#    @property
#    def anchorpoint(self):#returns center coord, created when graphicnode is created maybe?
#        pass
##        self.addNeighbors()
#    @property
#    def terminal(self):
#        pass
#    def changeGraphics(self,vals):
#        for i in vals.keys():
#            self.graphics[i]=vals
#        #@todo update graphics accordingly
#    def retqt(self,loc,color='red'):
#        if type(loc)==dict:
#            lx,ly=loc['x'],loc['y']
#        elif type(loc)==list or type(loc)==tuple:
#            lx,ly=loc
#        if self.graphic is None:
#            self.graphic=graphicNode
#        self.gnode=self.graphic(lx,ly,self.sz['x'],self.sz['y'],name=self.name,node=self)
#        
#        self.createTerminal()
##        self.createTerminal()
##        self.gnode.mouseReleaseEvent=lambda i:print(i.lastPos(),'test')
#        return self.gnode
#    def createTerminal(self,name='',loc=None,typ='out'):#@todo figure out if should refe rby loc or name
#        #terminal sz is 10, figure out math based on nodesize
#        #@todo different angles/colors based on direction type
#        tsz=10
#        startangle=-math.pi/2#angle (radians) added (CCW) from 0 (bottom)
#        N=self.nterm#number of terminals per node -"hours in day"
#        if len(self.terminals[typ])<N:
#            if loc is None:
#                cloc=((self.sz['x']+tsz)/2,(self.sz['y']+tsz)/2)#center position
#                ang=(2*math.pi/N*len(self.terminals[typ]))+startangle
#                loc=(cloc[0]+(self.sz['x']+tsz)/2*math.sin(ang),cloc[1]+(self.sz['y']+tsz)/2*math.cos(ang))#ugly but works
#                print(loc)
#            self.terminals[typ][loc]=Terminal(parent=self.gnode,loc=loc)
#            self.terminals[typ][loc].gterm.setParentItem(self.gnode)
#    def setFunction(self):#@todo redundant?
#        pass
#    #RECEIVE -> PROCESS -> SEND - override process in specific to prevent nodetype from sending signal further - not good idea to override send
#    def receiveSignal(self,value=None,source=None):
##        print(self,value)
#        self.processSignal(value=value,source=source) 
#    def processSignal(self,value,source=None):#does necessary processing here to make signal readable - changes based on class?
#       #use function here? or just have override to avoid hassles?
#       #does this need to have default value for source?
#       #base node should just act as relay 
##        print('base process activated') # used to debug if override is working 
#       #@todo figure out how to process signals needing more than one input
#        self.sendSignal(value)#shouldn't need to know source
#        
#    def sendSignal(self,value):
#        for e in self.edges.keys():
#            self.edges[e].edgeobj.carrySignal(self,value)
#   
#    def activateConnects(self):
#        pass
#    def addNeighbors(self,incids,outids):
#        ft={'in':incids,'out':outids}
#        for i in ft.keys():
#            
#            if type(ft[i])!=dict:
#                try: #if its sets or sm other iterable
#                    ft[i]={ii:{} for ii in ft[i]}
#                except:
#                    try:#prob number
#                        ft[i]={ft[i]:{}}
#                    except:#dunno what it is then
#                        raise
#                    
#            self.neighbors[i]=ft[i]
#            
class Terminal(object):
    def __init__(self,*args,parent=None,prop=None,node=None,name=None,loc=None):
        self.name=name
        self.parent=parent
        self.graphq(loc)
        
    def sendsignal(self):
        
       
        pass
    def hook(self):
        pass
    def unhook(self):
        pass
    def graphq(self,loc=None,color='white'):
       sz={'x':10,'y':10}#loc+sz=nodesz - get in middle
       self.gterm=Graphics.graphicTerminal(*loc,*sz.values(),parent=self.parent,name=self.name)
       
       self.gterm.setBrush(QtGui.QBrush(QtGui.QColor(color)))
#       print(self.gterm.parentItem())

class Edge(object):
    def __str__(self):
        return str(self.conn['from']) + " => " + str(self.conn['to'])
    def __init__(self,frm=None,to=None):
#        self.qt=QGraphicsLineItem
        self.neighbors=dict()#redundant?
        if frm is not None and to is not None:
            self.connectNodes(frm,to)
        else:
            self.conn={'from':'','to':''}#used for __str__ - inefficient?
#        self.conn=dict()
        #@todo make sure edge orientation decision is clear & graphically defined
    def carrySignal(self,source,signal):
        print(signal,source,self.conn['from'])
#        print(signal, 'received from ',source)

        if source==self.conn['from']:#prevents recursion
            self.conn['to'].receiveSignal(signal,source)
            
    def connectNodes(self,frm,to):
        
        print("connecting "+str(frm)+" to "+str(to))
        Node=Nodes.Node#@todo make less hacky
        if (type(frm)==Node or Node in type(frm).__bases__) and (type(to)==Node or Node in type(to).__bases__):
            self.conn={'from':frm,'to':to}
            return True
        else:
            self.conn={'from':'','to':''}
            return False
    def flipEdge(self):
        print('flipping')
        #redirects edge
        temp=self.conn
        self.conn={'from':temp['to'],'to':temp['from']}
        print('flipped rel' )