# -*- coding: utf-8 -*-
__version__='0.1.0'
"""
Created on Wed Aug 22 22:00:23 2018

help from 
ftp://ftp.ics.uci.edu/pub/centos0/ics-custom-build/BUILD/PyQt-x11-gpl-4.7.2/examples/graphicsview/diagramscene/diagramscene.py !!!!!!!!
http://www.windel.nl/?section=pyqtdiagrameditor
https://graphviz.gitlab.io/_pages/Documentation/TSE93.pdf
https://www.qtcentre.org/threads/5609-Drawing-grids-efficiently-in-QGraphicsScene
http://www.davidwdrell.net/wordpress/?page_id=46
https://stackoverflow.com/questions/3810245/how-to-select-multiple-items-without-pressing-ctrl-key-within-qgraphicsscene#3839127
https://stackoverflow.com/questions/32192607/how-to-use-itemchange-from-qgraphicsitem-in-qt/32198716#32198716
https://github.com/cb109/qtnodes
https://het.as.utexas.edu/HET/Software/html/graphicsview-elasticnodes.html
https://www.qtcentre.org/threads/43649-QGraphicsScene-is-SLOW-with-a-lot-of-items-!
https://adared.ch/qnodeseditor-qt-nodesports-based-data-processing-flow-editor/
https://stackoverflow.com/questions/20771965/qt-graph-drawing
http://blog.tjwakeham.com/pyqt4-node-editor/
https://github.com/rochus/qt5-node-editor
http://austinjbaker.com/node-editor-prototype
https://github.com/EricTRocks/pyflowgraph

0.
    0.2 - started logging
    0.3 - edges work & track
    1.0 - added first few special nodes, added (buggy) arrow, process flow substantiated, lots of modularization




TODO:
    Usable w/o gui
    Make signal its own object? - helpful to trace
    Make into Git
    constrainable lengths (blegh) - rigidity value 0-1 as some half tangent fn
    Datasources as Ngons? Torminals on points as distinct dims of data 
    create new connected node on click 
    hold on edge/terminal adjusts/dels? connections
    selectbox
    have startup net (customizable)
    Node types - 
        Circles - 
            "scoots over" as more terminals added
        Polygons
            -fixed # of nodes
            -sources?
        Boxes (rounded)
            clear distinction between in/out
        
    
    ctrl T on several nodes makes total connection (undir?)
    Drag & drop for nodes - long press to move, short to highlight, doubleclick to edit?
    Edges go from term(interface) to term, not nodes to nodes
    place nodes from forces/etc
    generate net from adjmat
    order of selection
    sub?terminal STDev 
    encode strength in size/aspect in color
    simplex coloring - low opacity & stacks
    clean up code
    max num of nodes able to b added (1000? - editable)
    select two nodes then key combo to add edge between em  (j?e?f?f?)
    keycombo for new nodes (a?shifta?)
    deleteable/breakable (x)
    "show network metrics"
    processing nodes
        start @ sources (data/topological sense)
        
    cache (short+long?) calculated paths/subpaths to save time - need to figure out how to handle different ways of inputting new data
    have custom "group" node as object w cache checkbox? 
    make able to "act like singularities" for DS? 
    
    
    
    
    
------
Each Network tracks all nodes & their connections - Animations/Edge Forces go here 
Each Node has a fn and has a list of terminals (shortcut to list of edges)
Each Terminal has list of edges "hooked" to` 
Each Edge knows From/To, Signal, and effect of edge (usually none if just transmission)

@todo implement bokeh for web dashboard
@todo merge array node 
@todo SQL nodes - pancake stack icon? - source automatically converts on detect


"""
import math

from PyQt5.QtWidgets import * #GUI (Graphical User Interface) library
from PyQt5 import QtGui, QtCore
#from pyqtgraph import flowchart
import numpy as np
import sys
from OHLib import *
#
class Network(object):#@todo able to save snapshot of page layout, make master controller which coordinates global stuff - nodes only know themselves and their terminals/edges, network knows bigger picture stuff
    def __init__(self):
        pass
    def saveNet(self):
        pass
    def loadNet(self):
        pass
    def forceModel(self,typ):    #do stuff like spring models here

        pass
    def isDirected(self):
        pass
    def toggleShowDirected(self):
        pass #saves directed data just mirrors matrix & keeps mags const 
        
    def transpose(self):
        pass
    
class Node(object):#baseclass for nodes - "dumb" & doesn't know who is connected to/[what type of edge (maybe bad idea?)], that's edges job
    #@todo define trigger here?
    def __str__(self):
        return str(self.__class__.__name__)+' '+str(self.name) #makes able to refer to node as "{Nodetype} {integer (unless name is otherwise changed)}" - ie "PrintNode 3" "PrintNode 5" "InputNode 9" ...- useful for debugging 
    def __init__(self,name,sz={'x':50,'y':50},slotless=False,fn=None,widget=None):
#        self.slots=dict()
        self.widget=widget
        
        self.qt=QGraphicsRectItem
        self.name=name
        self.sz=sz
        self.edges=dict()
        self.terminals=dict({'in':dict(),'out':dict()})#@todo make this the way to decide direction from node?b 
        defaultfn=lambda x:x#output is input
        if fn is not None:
            self.fn=fn
        else:
            self.fn=defaultfn
    def preprocess(self,values=None):
        pass
    @property
    def anchorpoint(self):#returns center coord, created when graphicnode is created maybe?
        pass
#        self.addNeighbors()
    @property
    def terminal(self):
        pass
    
    def retqt(self,loc,color='red'):
        if type(loc)==dict:
            lx,ly=loc['x'],loc['y']
        elif type(loc)==list or type(loc)==tuple:
            lx,ly=loc
        self.gnode=graphicNode(self.name,self,lx,ly,self.sz['x'],self.sz['y'])
        
        self.createTerminal()
#        self.createTerminal()
#        self.gnode.mouseReleaseEvent=lambda i:print(i.lastPos(),'test')
        return self.gnode
    def createTerminal(self,name='',loc=(20,0)):
        self.terminals[name]=Terminal(parent=self.gnode,loc=loc)
        self.terminals[name].gterm.setParentItem(self.gnode)
    def setFunction(self):#@todo redundant?
        pass
    #RECEIVE -> PROCESS -> SEND - override process in specific to prevent nodetype from sending signal further - not good idea to override send
    def receiveSignal(self,value=None,source=None):
#        print(self,value)
        self.processSignal(value=value,source=source) 
    def processSignal(self,value,source=None):#does necessary processing here to make signal readable - changes based on class?
       #use function here? or just have override to avoid hassles?
       #does this need to have default value for source?
       #base node should just act as relay 
#        print('base process activated') # used to debug if override is working 
       #@todo figure out how to process signals needing more than one input
        self.sendSignal(value)#shouldn't need to know source
        
    def sendSignal(self,value):
        for e in self.edges.keys():
            self.edges[e].edgeobj.carrySignal(self,value)
   
    def activateConnects(self):
        pass
    def addNeighbors(self,incids,outids):
        ft={'in':incids,'out':outids}
        for i in ft.keys():
            
            if type(ft[i])!=dict:
                try: #if its sets or sm other iterable
                    ft[i]={ii:{} for ii in ft[i]}
                except:
                    try:#prob number
                        ft[i]={ft[i]:{}}
                    except:#dunno what it is then
                        raise
                    
            self.neighbors[i]=ft[i]
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
       self.gterm=graphicTerminal(*loc,*sz.values(),parent=self.parent,name=self.name)
       
       self.gterm.setBrush(QtGui.QBrush(QtGui.QColor(color)))
#       print(self.gterm.parentItem())

class Edge(object):
    def __str__(self):
        return str(self.conn['from']) + " => " + str(self.conn['to'])
    def __init__(self,frm=None,to=None):
        self.qt=QGraphicsLineItem
        self.neighbors=dict()#redundant?
        if frm is not None and to is not None:
            self.connectNodes(frm,to)
        else:
            self.conn={'from':'','to':''}#used for __str__ - inefficient?
#        self.conn=dict()
        #@todo make sure edge orientation decision is clear & graphically defined
    def carrySignal(self,source,signal):
#        print(signal, 'received from ',source)

        if source==self.conn['from']:#prevents recursion
#            print(signal, ' sending to ',self.conn['to'])
            self.conn['to'].receiveSignal(signal,source)
            
    def connectNodes(self,frm,to):
        print("connecting "+str(frm)+" to "+str(to))
        if (type(frm)==Node or Node in type(frm).__bases__) and (type(to)==Node or Node in type(to).__bases__):
            self.conn={'from':frm,'to':to}
            return True
        else:
            return False
    def flipEdge(self):
#        print('flipping')
        #redirects edge
        temp=self.conn
        self.conn={'from':temp['to'],'to':temp['from']}
#Graphics should be kept separate from base model so can b run w/o gui 
###################################################     
   
class graphicNode(QGraphicsEllipseItem):

    def __init__(self,name,node,*arg):
        super(graphicNode,self).__init__(*arg)
        self.name=name
        self.nodeobj=node
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges,True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(5)
        
    def mouseReleaseEvent(self,*args):
        super(graphicNode,self).mouseReleaseEvent(*args)
        self.scene().nodeMoved.emit(self.name)
        
    def itemChange(self,change,value):
#        print(change,value)
#        super(graphicNode,self).itemChange(change,value)
        if change == QGraphicsItem.ItemPositionHasChanged:
#        
            self.scene().nodeMoved.emit(self.name)
        return QGraphicsItem.itemChange(self,change,value)
    def mouseDoubleClickEvent(self,*args):
        super(graphicNode,self).mouseDoubleClickEvent(*args)
#        print(*args)
#        else:
#    def mousePressEvent(self)
#        pass
#    def mouseMoveEvent(self):
#        pass
#    def mouseReleaseEvent(self):
#        pass
class graphicEdge(QGraphicsLineItem):
    def __init__(self,*arg,narr=None,edgeobj=None,**kwarg):
        super(graphicEdge,self).__init__(*arg,**kwarg)
        self.edgeobj=edgeobj
        if narr is not None:
            self.nodes=narr
        self.setAcceptHoverEvents(True)
#        self.setItem
#        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True) 
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        
#        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(10)
        
        p=self.pen()
        p.setWidth(3)
        p.setCapStyle(QtCore.Qt.RoundCap)
        self.setPen(p)
    def updatePos(self):
#        print(self.nodes.keys())
#        fp=self.nodes['from'].gnode.pos()
#        tp=self.nodes['to'].gnode.pos()
        
        lp=QtCore.QLineF(*(self.nodes[i].gnode.pos()+QtCore.QPointF(self.nodes[i].gnode.rect().size().height(),self.nodes[i].gnode.rect().size().width()) for i in ['from','to']))
        self.setLine(lp)
    def flipEdge(self):
        #make graphic flip
        self.edgeobj.flipEdge()

        
class arrowEdge(graphicEdge):
    def __init__(self,*arg,**kwarg):
        
        super(arrowEdge,self).__init__(*arg,**kwarg)
        self.arrowHead = QtGui.QPolygonF()
        
        
        self.headPoint=lambda:self.line().p2()
#        self.setPen(QtGui.QPen(QtGui.QColor('black') , 10, QtCore.Qt.SolidLine,
#                QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))

    def paint(self, painter, option, widget=None,**arg):
        arrowSize = 20.0
        p=painter.pen()
        p.setWidth(3)
        p.setCapStyle(QtCore.Qt.RoundCap)
        painter.setPen(p)
#        paintpen=self.pen()
#        paintpen.
        line = self.line()
        #@todo make arrowhead consistent
        #@todo 
#        print(line.length())
        angle = math.acos(line.dx() / max(line.length(),0.1))
        
        arrowP1 = self.headPoint() + QtCore.QPointF(math.sin(angle + math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi / 3) * arrowSize)
        arrowP2 = self.headPoint() + QtCore.QPointF(math.sin(angle + math.pi - math.pi / 3.0) * arrowSize,
                                        math.cos(angle + math.pi - math.pi / 3.0) * arrowSize)
        self.arrowHead.clear()
        for point in [self.headPoint(), arrowP1, arrowP2]:
            self.arrowHead.append(point)
        painter.drawLine(line)
        painter.drawPolygon(self.arrowHead)
        
        if self.isSelected():#draws bounding box
            boundwidth=10
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.DashLine))
            myLine = QtCore.QLineF(line)
            
            myLine.translate(0, boundwidth)
            painter.drawLine(myLine)
            myLine.translate(0,-2*boundwidth)#make more robust
            painter.drawLine(myLine)

    def shape(self,*arg):
        path=super(arrowEdge,self).shape(*arg) 
        path.addPolygon(self.arrowHead)
        return path
#        print(*arg)
#        addPolygon(QGraphicsPolygonItem(QtGui.QPolygonF([0,2,4])))
#        return p
#        pass
    def boundingRect(self,*arg,**kwarg):
         
        extra = (self.pen().width() + 20) / 2.0
        p1 = self.line().p1()
        p2 = self.line().p2()
        return QtCore.QRectF(p1, QtCore.QSizeF(p2.x() - p1.x(), p2.y() - p1.y())).normalized().adjusted(-extra, -extra, extra, extra)
    def flipEdge(self):
        super(arrowEdge,self).flipEdge()
        if self.headPoint()==self.line().p2():#@todo make less janky
            self.headPoint=lambda:self.line().p1()
        else:            
            self.headPoint=lambda:self.line().p2()
        self.update()
class graphicTerminal(QGraphicsEllipseItem):
    def __init__(self,*args,parent=None,name=None):
        super(graphicTerminal,self).__init__(*args,parent)
        self.setZValue(10)
#        self.setParentItem(parent)
        
        #tangent bezier?
         
    
        
##################################################
        #SPECIFIC NODE TYPES:
        #@todo - put default colors here? or maybe in network. not in window tho.
#@todo make sure everything plays nice with pandas - maybe numpy?
class AdditionNode(Node):
    def __init__(self,**kwargs):
        super(AdditionNode,self).__init__(fn=lambda x,y:x+y,**kwargs)
        self.signals=dict()
    def processSignal(self,value,source,**kwargs):#build source into basenode fn?
        #checks if has received enough signals to process, if not then waits/sends some sorta "not ready" signal? @todo - alla that
        try:#@todo make more flexible
            self.signals[source]=float(value)
        except:            
            print('not a number')#@todo emit some sorta error

        self.sendSignal(sum(self.signals.values()))
        
class SubtractionNode(Node):
    def __init__(self,**kwargs):
        super(SubtractionNode,self).__init__(**kwargs)
        self.signals=dict()
        self.sourceorder=[]#makes sure order is clear 
    def processSignal(self,value,source,**kwargs):#build source into basenode fn?
        #only can work with two inputs!!! 
        #@todo more elegant way of ensuring 
        #@todo mark which is first/second - terminal color?
        #@todo some way to ensure that dropped links are passed over in processing?
        try:
            self.signals[source]=float(value)
            if source not in self.sourceorder:
                self.sourceorder.append(source)
        except:
            print('not a number')
        
        try:
            dif=self.signals[self.sourceorder[0]]-self.signals[self.sourceorder[1]]
        except:
            try:
                dif=self.signals[self.sourceorder[0]]
            except:
                dif=0
        self.sendSignal(dif)
        
class PrintNode(Node):#@todo limit to one incoming connection, no limit on outgoing  ("glass pipe")
    def __init__(self,**kwargs):
        super(PrintNode,self).__init__(widget=QLabel(size=QtCore.QSize(50,10)),**kwargs)
    def processSignal(self,value,**kwargs):#overrides fn for custom behavior
        self.widget.setText(str(value))
        self.sendSignal(str(value))#optional?
#        print(value,' set')
class InputNode(Node):#make a QLineEdit appear in middle, takes as value
    def __init__(self,**kwargs):
        super(InputNode,self).__init__(widget=QLineEdit(),**kwargs)
        self.widget.setFixedWidth(30)
        self.value=self.widget.text
        self.widget.textChanged.connect(self.processSignal)
#        self.widget.textDel
#        proxy=QGraphicsProxyWidget(self)
#        proxy.setWidget(QLineEdit())
        
        
class SplitNode(Node):
    #@todo make sure node is still clickable somehow w bigger lists - move terminals automatically?
    def __init__(self,source=None,**kwargs):
        super(SplitNode,self).__init__(widget=QGroupBox(size=QtCore.QSize(30,50)),**kwargs)
        self.widget.setLayout(QVBoxLayout())
        self.btns=dict()
    #@returns only values from specified key, make dropdown, get preprocess working ok
#    @processSignal
    #@todo make toggling selection refire?
    def preprocess(self,values=None,source=None):#works with preprocess written as process
#        print('pre')
        if values is not None:
            for w in self.btns.values():
                self.widget.layout().removeWidget(w)
#                print('test',witem)
                w.setParent(None)
                
            for v in values:
                self.addOption(v[0])
                self.widget.layout().update()
        return processSignal(values)
#       pass
    @preprocess
    def processSignal(self,value=None,source=None):#shouldn't need to care abt source?
       print(value,self.widget.)
       
       return value
#        return value   
    
    def addOption(self,text):
        self.btns[text]=QRadioButton(text)
        self.widget.layout().addWidget(self.btns[text])
#        self.sendSignal(value)
        
class SourceNode(Node):
    def __init__(self,sourcefile=None,**kwargs):
        super(SourceNode,self).__init__(widget=QPushButton('select \nsource'),**kwargs)
        #@todo make button choose source, then when source is chosen display something different
        #@todo output format as dicts of values
        self.sourcefile=sourcefile
        f=self.widget.font()
        f.setPointSize(7)
        self.widget.setFont(f)
        self.widget.clicked.connect(lambda:self.chooseFile())
    def chooseFile(self,typ='db'):
        
        print('clicked')
        temp = QFileDialog.getOpenFileName(filter = typ+" files (*."+typ+")")
        self.sourcefile=temp
        if typ=='db':
            self.processSQL(self.sourcefile[0])
        else:
            print('whoops')
    def processSource(self):
        pass
    def checkSource(self):#checks if can read
        pass
    def processSQL(self,path):#redundant?
        c=sqlite3.connect(path)
        tables=c.execute("select name from sqlite_master where type='table'").fetchall()
        print(tables)
        self.sendSignal(tables)
#@todo make some sorta SQL Join friendly node to speed things up
class EndpointNode(Node):#outputs to some other process - JSON
    def __init__(self,**kwargs):
        pass
    
##################################################
class netWindow(QMainWindow):
    def __init__(self): 
        super(netWindow,self).__init__()
        self.wind=QWidget()
        self.setCentralWidget(self.wind)
        self.layout=QGridLayout()
        self.wind.setLayout(self.layout)
        
        self.Window()
        self.show()
        self.setMinimumSize(500,500)
    def Window(self):
        self.undir=False
        class gridscene(QGraphicsScene):
            nodeMoved=QtCore.pyqtSignal(int)
            def __init__(self,*args):
                super(gridscene,self).__init__(*args)
            def drawBackground(self,painter,rect,*args):
                pen=QtGui.QPen(QtGui.QColor('lightgray'))
                pen.setStyle(QtCore.Qt.DotLine)
                painter.setPen(pen)
                painter.drawLines(self.makebg())
            def makebg(self):
                gridsize=20
                lines=[]
        #        scene.
                
#                print(self.scene.sceneRect().right())
                mn,mx=-1000,1000
                ax,ay=50,50#anchor offset
                n=100
                for i in range(n):
                    
                    lines.append(QtCore.QLineF((i-ax)*gridsize,mn,(i-ax)*gridsize,mx))
                    
                    lines.append(QtCore.QLineF(mn,(i-ay)*gridsize,mx,(i-ay)*gridsize))
                return lines
        
        self.scene=gridscene()
        self.view=QGraphicsView(self.scene)
        self.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.layout.addWidget(self.view)
        self.toolbox=QToolBox()
#        self.toolbox.setMinimumWidth()
        self.nodes=dict()
        def updatenodefn(i,*args):
         
#            print(self.nodes[i].edges.keys())
            for j in self.nodes[i].edges.keys():
                if (i,j) in self.edges.keys():
                    self.edges[(i,j)].updatePos()
#                    print(self.edges.keys(),(j,i))
                else:
                    if (j,i) in self.edges.keys():
#                     print('test')
                     self.edges[(j,i)].updatePos()
       
        self.scene.nodeMoved.connect(updatenodefn)
#        self.scene.selectionChanged.connect(lambda:print(self.scene.selectedItems()))
        self.edges=dict()
        buttgrp=QGroupBox()
        buttgrp.setLayout(QHBoxLayout())
        self.btns=dict()
        def addBtn(text,fn,order=None):
            self.btns[text]=QPushButton(text=text)
            buttgrp.layout().addWidget(self.btns[text])
            self.btns[text].clicked.connect(fn)
            #@todo add a dropdown to group button types?   
        addBtn(text='source',fn=lambda:self.createNode(nodetype=SourceNode,color="#000000"))
        addBtn(text='split',fn=lambda:self.createNode(nodetype=SplitNode,color="fuchsia"))
        addBtn(text='+',fn=lambda:self.createNode(nodetype=AdditionNode,color="#ffffff"))
        addBtn(text='-',fn=lambda:self.createNode(nodetype=SubtractionNode,color="cyan"))
        addBtn(text='print',fn=lambda:self.createNode(nodetype=PrintNode,color="Pink"))
        addBtn(text='input',fn=lambda:self.createNode(nodetype=InputNode,color="#aaaaaa"))
        addBtn(text='node',fn=lambda:self.createNode(color=rainbow[len(self.nodes)%len(rainbow)]))
        addBtn(text='edge',fn=lambda:self.createConnect())
        addBtn(text='terminal',fn=lambda:self.scene.selectedItems()[0].nodeobj.createTerminal(loc=(0,20)))
        addBtn(text='delete',fn=lambda:self.deleteNode(self.scene.selectedItems()[0].nodeobj.name))#@todo make "name" vs "label" consistent)
        addBtn(text='flip',fn=lambda: self.scene.selectedItems()[0].flipEdge()) #@todo make able to check if selected object(s?) are edges before initiating flip

        self.layout.addWidget(buttgrp)
#        
    def generateAdjMat(self,root=0):
        n=len(self.nodes)
        A=np.zeros((n,n))
        for i in self.edges.keys():
            ii=(i[0]-1,i[1]-1)
            A[ii]=1
            if self.undir:
                A[ii[1],ii[0]]=1
        return A
            
   
    def createNode(self,nodetype=Node,label=None,defloc=None,color='red'):
        
        if label is None:
            label=len(self.nodes)+1
#            print(label)
        self.nodes[label]=nodetype(name=label)
        r=self.nodes[label].retqt((10,10))
        if self.nodes[label].widget is not None:
            proxy=QGraphicsProxyWidget(r)
            #@todo center graphicsproxy
            proxy.setZValue(999)#should display on top no matter what
            proxy.setWidget(self.nodes[label].widget)
#        print(r)
        r.setBrush(QtGui.QBrush(QtGui.QColor(color)))
        self.scene.addItem(r)
#        print(self.generateAdjMat())
        
    def createConnect(self,nfrom=1,nto=2):
        if len(self.scene.selectedItems())==2:#if selection is obvious  ---- can do smth w selectionChanged to figure out order selected for from/to
            nfrom,nto=[i.name for i in self.scene.selectedItems()]
        narr=(nfrom,nto)
        nd={'from':self.nodes[nfrom],'to':self.nodes[nto]}
#        xto,yto=senarr=ndlf.nodes[nto].gnode.pos()
#        xfrom,yfrom=self.nodes[nfrom].gnode.pos()
        if narr in self.edges.keys():#checks if refers right
#        
            self.edges[narr].updatePos()
#            self.scene.removeItem(self.edges[narr])
            edge=self.edges[narr]
        else:#@todo clean up this fn
            edgeobj=Edge(self.nodes[nfrom],self.nodes[nto])
            edge=arrowEdge(self.nodes[nfrom].gnode.x()+self.nodes[nfrom].sz['x'],self.nodes[nfrom].gnode.y()+self.nodes[nfrom].sz['y'],self.nodes[nto].gnode.x()+self.nodes[nfrom].sz['x'],self.nodes[nto].gnode.y()+self.nodes[nfrom].sz['y'],narr=nd,edgeobj=edgeobj)
#        edge.setParentItem(self.nodes[1].gnode)
        self.edges[(nfrom,nto)]=edge
        self.nodes[nfrom].edges[nto]=edge
#        rpg
        self.nodes[nto].edges[nfrom]=edge
        
        self.scene.addItem(edge)
#        print(self.edges)
#        print(self.generateAdjMat())
       
    def breakConnect(self,nfrom,nto):
        pass
    def deleteNode(self,label):
        print(label)
        pass
    #@todo flesh out deletenode
    
    
    
    
    
    
    
    
    
    
def netrun():
    app=0         
    #windthread=QtCore.QThread()
    
    app=QApplication(sys.argv)
    wind=netWindow()
    app.exec_()
rainbow
    
    
    
    
types=['sources','fns','restricts','categories','outputs']
{'fns':{'meta':{},'add':{},'sub':{}},
 'outputs':{'heatmap','scatterrel','timeline'},
 'restricts':{'single','quotient/category','range'}}