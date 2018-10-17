# -*- coding: utf-8 -*-
"""
Do all custom node definitions here, import to main module
"""
import numpy as np
import sys
from OHLib import *
import .Base

class AdditionNode(Node):
    def __init__(self,**kwargs):
        super(AdditionNode,self).__init__(fn=lambda x,y:x+y,graphic=defnode,**kwargs)
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
        super(SubtractionNode,self).__init__(nterm=3,graphic=defnode,**kwargs)
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
class AverageNode(Node):
    def __init__(self,*args,**kwargs):
        super(AverageNode,self).__init__(*args,**kwargs)
        self.signals=dict()
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
        super(PrintNode,self).__init__(nterm=2,graphic=defnode,widget=QLabel(size=QtCore.QSize(50,10)),**kwargs)
    def processSignal(self,value,**kwargs):#overrides fn for custom behavior
        self.widget.setText(str(value))
        self.sendSignal(str(value))#optional?
#        print(value,' set')
        
class StepperNode(Node):#steps through array one value at a time - useful?
    def__init__(self,**kw):
        super(StepperNode,self).__init__(**kw)
class InterfaceNode(Node):
    def __init__(self,**kw):
        super(InterfaceNode,self).__init__(**kw)
        #gets info from some other qtgui & runs on headless mode by default  -  includes endpoint?
class InputNode(Node):#@TODO BUG - QLIneedit not working
    def __init__(self,**kwargs):
        super(InputNode,self).__init__(nterm=1,graphic=defnode,widget=QLineEdit(),**kwargs)
        self.widget.setFixedWidth(30)
        self.value=self.widget.text
        self.widget.textChanged.connect(self.processSignal)
#        self.widget.textDel
#        proxy=QGraphicsProxyWidget(self)
#        proxy.setWidget(QLineEdit())
class DateSplitNode(Node):
    def __init__(self,source=None,**kw):
        super(DateSplitNode,self).__init__(**kw)
        self.ndays=QLineEdit()#input 
        self.phase=''#<=ndays - changes startingday
class SplitNode(Node):#@todo make each option given connect to a terminal instead of having to choose
    #@todo make sure node is still clickable somehow w bigger lists  - padding?
    def __init__(self,source=None,**kwargs):
        super(SplitNode,self).__init__(widget=QGroupBox(size=QtCore.QSize(30,50)),graphic=defnode,**kwargs)
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
#        return processSignal(values)
#       pass
#    @preprocess
    def processSignal(self,value=None,source=None):#shouldn't need to care abt source?
#       print(value,self.widget.)
       
       return value
#        return value   
    
    def addOption(self,text):
        self.btns[text]=QRadioButton(text)
        self.widget.layout().addWidget(self.btns[text])
#        self.sendSignal(value)

        #test
        #@todo make whole Pancakes selectable

class SourceNode(Node):
    def __init__(self,sourcefile=None,**kwargs):
        super(SourceNode,self).__init__(widget=QPushButton('select \nsource'),graphic=graphicPancakes,**kwargs)
        #@todo make button choose source, then when source is chosen display something different
        #@todo output format as dicts of values
        self.sourcefile=sourcefile
        f=self.widget.font()
        f.setPointSize(7)
        self.widget.setFont(f)
        self.widget.setMaximumWidth(30)
        self.widget.clicked.connect(lambda:self.chooseFile())
    def chooseFile(self,typ='db'):
        
        print('clicked')
        temp = QFileDialog.getOpenFileName(filter = typ+" files (*."+typ+")")
        self.sourcefile=temp
        if typ=='db':
            self.processSQL(self.sourcefile[0])
        else:
            print('whoops')#@todo something to ensure that terminal and widget(s) don't overlap
    def processSource(self):
        pass
    def checkSource(self):#checks if can read
        pass
    def processSQL(self,path):#redundant?
        c=sqlite3.connect(path)
        tables=c.execute("select name from sqlite_master where type='table'").fetchall()
        print(tables)
        self.sendSignal(tables)
class RollingAverageNode(Node):
    def __init__(self,**kw):
        pass
class SQLCommandNode(Node):#@todo make pancake borders dependent on npan
    def __init__(self,sourcefile=None,**kwargs):
        def pancakefn(*args,**kwargs):#ugly but works - returns single pancake
            return graphicPancakes(*args,**kwargs,color='blue',npan=1)
        super(SQLCommandNode,self).__init__(widget=QLabel('WHERE'),graphic=pancakefn,**kwargs)
        commands={'WHERE':{'color':'red'},
                  'SELECT':{'color':'blue'},
                  'JOIN':{'color':'green'},
                  'AND/OR/NOT':{'color':'purple'},
                  'MIN/MAX':{'color':'yellow'},
                  'COUNT/AVG/SUM':{'color':'black'},
                  'IN':{'color':'white'},
                  'LIKE':{'color':'pink'}}
        
class HoloviewGraphNode(Node):
    def __init__(self,**kw):
        #tries to figure out based on input
        super(BokehGraphNode,self).__init__(**kw)
        types=dict('Bars':{},'Scatter':{})
        #incoming terminals: basedims[max(2)] sliderdims[N] overlaydims[<=N]
        #outgoing terminals: layout object (bokeh/matplotlib) - connect to endpoint
class SliceNode(Node):#breaks data into quotients based on some attribute (date (breaks down into custom len), item, donor, whatever)
    pass
class EndpointNode(Node):#outputs to some other process - JSON?
    def __init__(self,**kwargs):
        pass
    
    #inputbox of endpoint name
    #@todo two edges selected e to add edge