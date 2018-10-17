# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 20:45:03 2018

@author: V
"""
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import * #GUI (Graphical User Interface) library
#Graphics should be kept separate from base model so can b run w/o gui  test
###################################################     
   
class graphicNode(QGraphicsEllipseItem):

    def __init__(self,*arg,name=None,node,**kwarg):
        super(graphicNode,self).__init__(*arg,**kwarg)
        self.name=name
        self.nodeobj=node
        self.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine))
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
#@todo on select make node's pen turn dotted instead of square?

class graphicEdge(QGraphicsLineItem):
    def __init__(self,*arg,narr=None,edgeobj=None,fromobj=None,toobj=None,**kwarg):
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
    def __init__(self,*args,parent=None,name=None,scene=None):
        super(graphicTerminal,self).__init__(*args,parent)
        self.scene=scene
        self.setZValue(10)
        #@todo make slideable around border?
        
#        self.setFlag(QGraphicsItem.ItemIsMovable, True) 
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges,True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setAcceptHoverEvents(True)
#        self.setParentItem(parent)
        
        #@todo tangent bezier
        
        
        #@todo click and drag on terminal makes an edge coming from it 
        
    def hoverEnterEvent(self,event,*args,**kwargs):
#        print('entered')
        pass
#        if type(self.scene.selectedItems()[0])==Terminal:
#            print('terminal')
#        else:
#            print(self.scene.selectedItems()[0])
    def hoverLeaveEvent(self,event,*args,**kwargs):
        
        pass
    
    def mousePressEvent(self,event,*args,**kwargs):
        print('press',event)
        #create edge
        self.moved=False
        
        
    def mouseMoveEvent(self,event,*args,**kwargs):
        print('move',event)
        self.moved=True
        
    def mouseReleaseEvent(self,event,*args,**kwargs):
        dropradius=10
        if self.moved:
            #drop
            pass
        else:
            pass
            #remove without doing anything
    
class graphicPancakes(graphicNode):#used for SQL databases
    def __init__(self,*args,node=None,npan=3,name=None,pheight=10,color=None,pwidth=50,gap=18,perspective=3,**kwargs):
        super(graphicPancakes,self).__init__(*args,node=node,name=name,**kwargs)
#        topcirc=QGraphicsEllipseItem()
#        self.name=name
        self.persp=perspective
        self.width=pwidth
        
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.height=pheight
        self.gap=gap
        self.N=npan
        colors={'red':{'top':'#ff0000','bott':"#aa4444"},
                       'blue':{'top':"#26a8d3",'bott':"#2651d3"},
                      None:{'top':'#aaaaaa','bott':"#dddddd"}}
        self.color=colors[color]
            
#        self.setBrush(QtGui.QBrush(QtGui.QColor("#fffa00")))
#        QGraphicsObject.
#        self.setPen(QtGui.QPen(QtCore.Qt.black, 3, QtCore.Qt.SolidLine))
    def paint(self,painter,option,*args,**kwargs):
        for i in range(self.N):
            
            self.createCylinder(painter,loc={'x':0,'y':0-i*self.gap})
        if self.isSelected():#draws bounding box
            boundwidth=20
            print('test')
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.DashLine))
            painter.setBrush(QtCore.Qt.NoBrush)
            bline=QtCore.QRectF(0-.5*boundwidth,-2*self.width/self.persp-boundwidth,self.width+boundwidth,4*self.width/self.persp+boundwidth)
            #@todo make sure Pancakes is centered
            painter.drawRect(bline)
    def createCylinder(self,painter,loc={'x':0,'y':0}):

        topcolor=QtGui.QColor(self.color['top'])
        bottcolor=QtGui.QColor(self.color['bott'])
        print(loc,self.height,self.width,self.gap)
        topcirc=QGraphicsEllipseItem(loc['x'],loc['y'],self.width,self.width/self.persp)
        bottcirc=QGraphicsEllipseItem(loc['x'],loc['y']+self.height,self.width,self.width/self.persp)

        painter.setBrush(QtCore.Qt.SolidPattern)
        painter.setBrush(bottcolor)
        painter.drawPath(bottcirc.shape())
        
        painter.setBrush(topcolor)
        painter.drawPath(topcirc.shape())
        
        ybase=loc['y']+self.width/(self.persp*2)
        
        painter.drawLine(loc['x']+self.width,ybase,loc['x']+self.width,ybase+self.height)
        painter.drawLine(loc['x'],ybase,loc['x'],ybase+self.height)
    def boundingRect(self):
         return QtCore.QRectF(-20,-3*self.width/self.persp-30,40+self.width,6*self.width/self.persp+30)#@todo make less janky
#        bottcirc.setStartAngle(180*16)#in units of 16th of a degree for some reason - unneccessary?
#        bottcirc.setSpanAngle(180*16)