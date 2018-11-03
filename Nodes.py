# -*- coding: utf-8 -*-
"""

"""
#@todo "Quotient" groups
import numpy as np
import sys
import math

from OHLib import *

from PyQt5.QtWidgets import * 
import PyQt5.QtCore as QtCore#@todo make non-reliant on qt
import Graphics
import Objects
#from Objects import Node
#import .Base
# btndict={'inputs':{'inputbox':lambda:self.createNode(nodetype='InputNode',color="#aaaaaa"),
#                          'source':lambda:self.createNode(nodetype='SourceNode',color="#000000")},
#                 'filters':{'SQL':lambda:self.createNode(nodetype='SQLCommandNode',color='Red'),
#                            'split':lambda:self.createNode(nodetype='SplitNode',color="fuchsia")},
#                 'math':{'+':lambda:self.createNode(nodetype='AdditionNode',),
#                         '-':lambda:self.createNode(nodetype='SubtractionNode',color="cyan"),
#                         'average':lambda:self.createNode(nodetype='AverageNode',color="#987654")},
#                 'basics':{'node':lambda:self.createNode(color=rainbow[len(self.nodes)%len(rainbow)]),
#                           'edge':lambda:self.connectNodes(),
#                           'terminal':lambda:self.scene.selectedItems()[0].nodeobj.createTerminal()},
#                 'utils':{'delete':lambda:self.deleteNode(self.scene.selectedItems()[0].nodeobj.name),
#                          'flip':lambda: self.scene.selectedItems()[0].flipEdge()},
#                 'outputs':{'print':lambda:self.createNode(nodetype='PrintNode',color="Pink")},
#                'SQL':{},
#                'arraytools':{},
#                'HoloViews tools':{},#@todo show as tree-view if somehow is indicated w parent
#                }#@todo make able to check if selected object(s?) are edges before initiating flip
#        
#Node=Objects.Node
#
class Node(object):#baseclass for nodes - "dumb" & doesn't know who is connected to/[what type of edge (maybe bad idea?)], that's edges job
    #@todo define trigger here?
    def __str__(self):
        return str(self.__class__.__name__)+' '+str(self.name) #makes able to refer to node as "{Nodetype} {integer (unless name is otherwise changed)}" - ie "PrintNode 3" "PrintNode 5" "InputNode 9" ...- useful for debugging 
    def __init__(self,name,sz={'x':50,'y':50},nterm=10,slotless=False,fn=None,widget=None,graphic=None):
#        self.slots=dict()
        self.widget=widget
        self.nterm=nterm
        self.graphics={'graphicobj':'graphicNode',
                       'btnlabel':''}
#        self.qt=QGraphicsRectItem
        self.name=name
        self.graphic=graphic
        self.sz=sz
        self.edges=dict()
        self.terminals=dict({'in':dict(),'out':dict()})#@todo make this the way to decide direction from node?b 
        defaultfn=lambda x:x#output is input
        if fn is not None:
            self.fn=fn
        else:
            self.fn=defaultfn
    def nodeReady(self,*a,**kw):
        print(kw)
    def preprocess(self,values=None):
        pass
    @property
    def anchorpoint(self):#returns center coord, created when graphicnode is created maybe?
        pass
#        self.addNeighbors()
    @property
    def terminal(self):
        pass
    def addGraphics(self,vals):
        for i in vals.keys():
            self.graphics[i]=vals
        #@todo update graphics accordingly
    def retqt(self,loc,color='red'):
        if type(loc)==dict:
            lx,ly=loc['x'],loc['y']
        elif type(loc)==list or type(loc)==tuple:
            lx,ly=loc
        if self.graphic is None:
            self.graphic=Graphics.graphicNode
        self.gnode=self.graphic(lx,ly,self.sz['x'],self.sz['y'],name=self.name,node=self)
        
        self.createTerminal()
#        self.createTerminal()
#        self.gnode.mouseReleaseEvent=lambda i:print(i.lastPos(),'test')
        return self.gnode
    def createTerminal(self,name='',loc=None,typ='out'):#@todo figure out if should refe rby loc or name
        #terminal sz is 10, figure out math based on nodesize
        #@todo different angles/colors based on direction type
        tsz=10
        startangle=-math.pi/2#angle (radians) added (CCW) from 0 (bottom)
        N=self.nterm#number of terminals per node -"hours in day"
        if len(self.terminals[typ])<N:
            if loc is None:
                cloc=((self.sz['x']+tsz)/2,(self.sz['y']+tsz)/2)#center position
                ang=(2*math.pi/N*len(self.terminals[typ]))+startangle
                loc=(cloc[0]+(self.sz['x']+tsz)/2*math.sin(ang),cloc[1]+(self.sz['y']+tsz)/2*math.cos(ang))#ugly but works
                print(loc)
            self.terminals[typ][loc]=Objects.Terminal(parent=self.gnode,loc=loc)
            self.terminals[typ][loc].gterm.setParentItem(self.gnode)
    def setFunction(self):#@todo redundant?
        pass
    #RECEIVE -> PROCESS -> SEND - override process in specific to prevent nodetype from sending signal further - not good idea to override send
    def receiveSignal(self,value=None,source=None):
#        print(self,value)
        print('rec '+str(value))
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
     

class AdditionNode(Node):
    def __init__(self,**kwargs):
        super(AdditionNode,self).__init__(fn=lambda x,y:x+y,graphic=Graphics.graphicNode,**kwargs)
        self.signals=dict()
        self.addGraphics({'btnlabel':'+','color':"#ffffff"})
    def processSignal(self,value,source,**kwargs):#build source into basenode fn?
        #checks if has received enough signals to process, if not then waits/sends some sorta "not ready" signal? @todo - alla that
        try:#@todo make more flexible
            self.signals[source]=float(value)
        except:            
            print('not a number')#@todo emit some sorta error

        self.sendSignal(sum(self.signals.values()))
        
class SubtractionNode(Node):
    def __init__(self,**kwargs):
        super(SubtractionNode,self).__init__(nterm=3,graphic=Graphics.graphicNode,**kwargs)
        self.signals=dict()
        self.addGraphics({'btnlabel':'-','color':"#ffffff"})
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
class AverageNode(Node):
    def __init__(self,*args,**kwargs):
        super(AverageNode,self).__init__(*args,**kwargs)
        self.signals=dict()
     
        self.addGraphics({'btnlabel':'Average','color':"#ffffff"})

    def processSignal(self,value,source,**kwargs):#needs to be able to handle an array/handles inputs clearly defined 
        #default unit is array, ordered lists assumed to be arrays, single values are assumed as 1d arrays, sets are auto-averaged and then handled as 1-d arrays
        #if handed numbers from several nodes: take as one-dim arrays
        #if handed single array: average that array
        #if handed multiple arrays of same length: average of each value within array (generalizes to 1 d)
        if type(value)==set:
            self.signals[source]=[np.average(value)]
        elif type(value) in [list,np.array,tuple]:
            self.signals[source]=[]
        else:
            print('not an understandable format')
class PrintNode(Node):#@todo limit to one incoming connection, no limit on outgoing  ("glass pipe")
    def __init__(self,**kwargs):
        super(PrintNode,self).__init__(nterm=2,graphic=Graphics.graphicNode,widget=QLabel(size=QtCore.QSize(50,10)),**kwargs)
        self.addGraphics({'btnlabel':'Print','color':"#ffffff"})
    def processSignal(self,value,**kwargs):#overrides fn for custom behavior
        print('incoming '+str(value))
        self.widget.setText(str(value))
        self.sendSignal(str(value))#optional?
#        print(value,' set')
        
class StepperNode(Node):#steps through array one value at a time - useful?
    def __init__(self,**kw):
        super(StepperNode,self).__init__(**kw)
        self.addGraphics({'btnlabel':'+','color':"#ffffff"})
class InterfaceNode(Node):
    def __init__(self,**kw):
        super(InterfaceNode,self).__init__(**kw)
        self.addGraphics({'btnlabel':'+','color':"#ffffff"})
        #gets info from some other qtgui & runs on headless mode by default  -  includes endpoint?
class InputNode(Node):#@TODO BUG - QLIneedit not working
    def __init__(self,**kwargs):
        super(InputNode,self).__init__(nterm=1,graphic=Graphics.graphicNode,widget=QLineEdit(),**kwargs)
        self.widget.setFixedWidth(30)
        self.value=self.widget.text
        self.widget.textChanged.connect(self.processSignal)
        self.addGraphics({'btnlabel':'Input','color':"#ffffff"})
#        self.widget.textDel
#        proxy=QGraphicsProxyWidget(self)
#        proxy.setWidget(QLineEdit())
        #@todo some easy way of saying in-node that is ready?
class DateSplitNode(Node):
    def __init__(self,source=None,**kw):
        super(DateSplitNode,self).__init__(**kw)
        self.addGraphics({'btnlabel':'Split (Date)','color':"#ffffff"})
        self.ndays=QLineEdit()#input 
        self.phase=''#<=ndays - changes startingday
class SplitNode(Node):#@todo make each option given connect to a terminal instead of having to choose
    #@todo make sure node is still clickable somehow w bigger lists  - padding?
    def __init__(self,source=None,**kwargs):
        super(SplitNode,self).__init__(widget=QGroupBox(size=QtCore.QSize(30,50)),graphic=Graphics.graphicNode,**kwargs)
        self.widget.setLayout(QVBoxLayout())
        self.addGraphics({'btnlabel':'Split','color':"#ffffff"})
        self.btns=dict()
    #@returns only values from specified key, make dropdown, get preprocess working ok
#    @processSignal
    #@todo make toggling selection refire?
    def processSignal(self,values=None,source=None):#works with preprocess written as process
#        print('pre')
        if values is not None:
            for w in self.btns.values():
                self.widget.layout().removeWidget(w)
#                print('test',witem)
                w.setParent(None)
                
            for v in values:
                self.addOption(v[0])
                self.widget.layout().update()
#        return processSignal(values)
#       pass
##    @preprocess #@todo figure this all out
#    def processSignal(self,value=None,source=None):#shouldn't need to care abt source?
##       print(value,self.widget.)
#       
#       return value
##        return value   
#    
    def addOption(self,text):
        self.btns[text]=QRadioButton(text)
        self.widget.layout().addWidget(self.btns[text])
#        self.sendSignal(value)

        #test
        #@todo make whole Pancakes selectable

class SourceNode(Node):
    #@todo outputs: SQL, (Pandas) Array, Tables
    
    def __init__(self,sourcefile=None,**kwargs):
        super(SourceNode,self).__init__(widget=QPushButton('select \nsource'),graphic=Graphics.graphicPancakes,**kwargs)
        self.addGraphics({'btnlabel':'Source','group':'Inputs','color':"#ffffff"})
        #@todo make button choose source, then when source is chosen display something different
        #@todo output format as dicts of values
        self.sourcefile=sourcefile
        f=self.widget.font()
        f.setPointSize(7)
        self.widget.setFont(f)
        self.widget.setMaximumWidth(30)
        self.widget.clicked.connect(lambda:self.chooseFile())
    def chooseFile(self,typ='db'):
        
#        print('clicked')
        temp = QFileDialog.getOpenFileName(filter = typ+" files (*."+typ+")")
        self.sourcefile=temp
        if typ=='db':
            self.processSQL(self.sourcefile[0])
        else:
            print('whoops')#@todo something to ensure that terminal and widget(s) don't overlap
    def processSource(self):#
        pass
    def checkSource(self):#checks if can read
        pass
    def processSQL(self,path):#redundant?
        c=sqlite3.connect(path)
        tables=c.execute("select name from sqlite_master where type='table'").fetchall()
#        print(tables)
        self.sendSignal(tables)
class RollingAverageNode(Node):
    def __init__(self,**kw):
        pass
class ArrayNode(Node):
    pass
class SQLCommandNode(Node):#@todo make pancake borders dependent on npan
    def __init__(self,cmd='WHERE',sourcefile=None,**kwargs):
        def pancakefn(*args,**kwargs):#ugly but works - returns single pancake
            return Graphics.graphicPancakes(*args,**kwargs,color='blue',npan=1)
        super(SQLCommandNode,self).__init__(widget=QLabel(str(cmd)),graphic=pancakefn,**kwargs)
        commands={'WHERE':{'color':'red'},
                  'SELECT':{'color':'blue'},
                  'JOIN':{'color':'green'},
                  'AND/OR/NOT':{'color':'purple'},
                  'MIN/MAX':{'color':'yellow'},
                  'COUNT/AVG/SUM':{'color':'black'},
                  'IN':{'color':'white'},
                  'LIKE':{'color':'pink'}}
        self.addGraphics({'btnlabel':'SQL','color':commands[cmd]})
class AggregateDataNode(Node):
    pass
#if data is in same format then aggregates into one pandas dataframe - multiple options for duplicate data
        
class StreamNode(Node):
#    self.btnlabel='Stream'
    pass #@todo include "latency" param?
#Extensions? 
        #TensorFlow?
        #have a "hook" for graphicsicon? 
#Colorlist/Colormap node       
        #Jupyter output?
#@todo make OH-specific default table reading nodes/default tables
        #@todo have a way of telling if tables are "wide" - column per item or "tidy" - column per attribute
class HoloviewGraphNode(Node):
    def __init__(self,**kw):
        self.addGraphics({'btnlabel':'HoloViews Graph','color':"#ffffff"})
        #tries to figure out based on input
        super(BokehGraphNode,self).__init__(**kw)
        types={'Bars':{},'Scatter':{},'Heatmap':{}}
        #incoming terminals: basedims[max(2)] sliderdims[N] overlaydims[<=N]
        #outgoing terminals: layout object (bokeh/matplotlib) - connect to endpoint
class SliceNode(Node):#breaks data into quotients based on some attribute (date (breaks down into custom len), item, donor, whatever)
    pass
class GroupNode(Node):
    pass
class EndpointNode(Node):#outputs to some other process - JSON?
    def __init__(self,**kwargs):
        self.btnlabel='Endpoint'
        self.addGraphics({'btnlabel':'Endpoint','color':"#ffffff"})
        
    #inputbox of endpoint name
    #@todo two edges selected e to add edge
