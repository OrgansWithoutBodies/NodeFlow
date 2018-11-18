# -*- coding: utf-8 -*-
"""
All the handling of window/graphicsscene events - immediately downstream of graphics
"""

import math

from PyQt5.QtWidgets import * #GUI (Graphical User Interface) library
from PyQt5 import QtGui, QtCore
#from pyqtgraph import flowchart
import numpy as np
import sys

from OHLib import *
import Graphics

#@todo box-select
class netWindow(QMainWindow):
    def __init__(self,net,**kw): 
        super(netWindow,self).__init__(**kw)
        self.net=net
        self.wind=QWidget()
        self.setCentralWidget(self.wind)
        self.layout=QGridLayout()
        self.wind.setLayout(self.layout)
#        QtGui.QShortcutEvent()
        self.Window()
        self.show()
        self.setMinimumSize(500,500)
    def Window(self):
        self.undir=False
        class gridscene(QGraphicsScene):
            nodeMoved=QtCore.pyqtSignal(int)
            def __init__(self,*args):
                super(gridscene,self).__init__(*args)
                self.keylist=[]
            def keyPressEvent(self,event):
                self.firstRelease=True
                self.keylist.append(event.key())#16777248 shift
                if QtCore.Qt.ShiftModifier in self.keylist:
                    
#                    print('shift')
#                    if 
                    print([i for i in self.keylist])
#                    print(event.count())
            def keyReleaseEvent(self,event):
                if self.firstRelease==True:
#                    print(self.keylist)
                    pass
                self.firstRelease=False
#                del self.keylist[-1]#dont remember what this was doing
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
#        self.scene.addItem(graphicPancakes())
        self.view=QGraphicsView(self.scene)
#        short=QtGui.QShortcutEvent(QtGui.QKeySequence("Shift+A"),self.view)
#        short.activated.connect(lambda:print('testing'))
        self.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.layout.addWidget(self.view)
        self.toolbox=QToolBox()
#        self.toolbox.setMinimumWidth()
        self.nodes=dict()
        def updatenodefn(i,*args):#updates position of all edges connected to this node
#            print('test',self.nodes[i].edges)
            for j in self.nodes[i].edges.keys():#step through all edges connected to this note
                if (i,j) in self.net.edges.keys():#
                    self.net.edges[(i,j)].updatePos()
#                    print(self.edges.keys(),(j,i))
                else:
                    if (j,i) in self.net.edges.keys():
#                     print('test')
                        self.net.edges[(j,i)].updatePos()
       
        self.scene.nodeMoved.connect(updatenodefn)
#        self.scene.selectionChanged.connect(lambda:print(self.scene.selectedItems()))
        self.edges=dict()
        buttgrp=QGroupBox()
        buttgrp.setLayout(QHBoxLayout())
        self.btns=dict()
        self.grps=dict()
        self.btnfns=dict()
        def addBtn(text,fn,grp=None,order=None):
            self.btnfns[text]=fn
            if grp is None:
                self.btns[text]=QPushButton(text=text)
                self.btns[text].clicked.connect(self.btnfns[text])
                buttgrp.layout().addWidget(self.btns[text])
            else:
                if grp not in self.grps.keys():
                    self.grps[grp]=QComboBox()
                    buttgrp.layout().addWidget(self.grps[grp])
                    self.grps[grp].addItem(grp.upper()+' group')      
                    self.grps[grp].activated[str].connect(lambda i:self.btnfns[i]())
                
                self.grps[grp].addItem(text)
                #@todo have a label area on page for errors
            #@todo make a "repeat action" per group?
            #add all buttons here
            #{groupname:{buttonname:fn}}
#        for n in self.net.availableNodes:
        btndict={'inputs':{'inputbox':lambda:self.createNode(nodetype='InputNode',color="#aaaaaa"),
                          'source':lambda:self.createNode(nodetype='SourceNode',color="#000000")},
                 'filters':{'SQL':lambda:self.createNode(nodetype='SQLCommandNode',color='Red'),
                            'split':lambda:self.createNode(nodetype='SplitNode',color="fuchsia")},
                 'math':{'+':lambda:self.createNode(nodetype='AdditionNode',color="#ffffff"),
                         '-':lambda:self.createNode(nodetype='SubtractionNode',color="cyan"),
                         'average':lambda:self.createNode(nodetype='AverageNode',color="#987654")},
                 'basics':{'node':lambda:self.createNode(color=rainbow[len(self.nodes)%len(rainbow)]),
                           'edge':lambda:self.createConnect(),
                           'terminal':lambda:self.scene.selectedItems()[0].nodeobj.createTerminal()},
                 'utils':{'delete':lambda:self.deleteNode(self.scene.selectedItems()[0].nodeobj.name),
                          'flip':lambda: self.scene.selectedItems()[0].flipEdge()},
                 'outputs':{'print':lambda:self.createNode(nodetype='PrintNode',color="Pink")},
                'SQL':{},
                'arraytools':{},
                'HoloViews tools':{},#@todo show as tree-view if somehow is indicated w parent
                }#@todo make able to check if selected object(s?) are edges before initiating flip
        for g in btndict.keys():
            for t in btndict[g].keys():
                addBtn(grp=g,text=t,fn=btndict[g][t])
        self.layout.addWidget(buttgrp)
#        
    
   #@todo make this syntax less confusing wrt here vs Network attributes - drawNode?
    def createNode(self,label=None,defloc=None,color='red',**kw):
        if label is None:
            label=len(self.nodes)+1
        self.nodes[label]=self.net.createNode(label=label,**kw)#creates actual node object which then gets rendered
        
#        self.nodes[label]=nodetype(name=label)
        r=self.nodes[label].retqt(loc=(10,10))
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
#        nd={'from':self.nodes[nfrom],'to':self.nodes[nto]}
#        xto,yto=senarr=ndlf.nodes[nto].gnode.pos()
#        xfrom,yfrom=self.nodes[nfrom].gnode.pos()
        if narr in self.net.edges.keys():#checks if refers already
#        
            self.net.edges[narr].updatePos()
#            self.scene.removeItem(self.edges[narr])
            edge=self.net.edges[narr]
        else:#@todo clean up this fn
            edge=self.net.connectNodes(nfrom,nto)
#        edge.setParentItem(self.nodes[1].gnode)
           
        self.scene.addItem(edge)
#        print(self.edges)
#        print(self.generateAdjMat())
       
    def breakConnect(self,nfrom,nto):
        pass
    def deleteNode(self,label):
        print(label)
        pass
    #@todo flesh out deletenode