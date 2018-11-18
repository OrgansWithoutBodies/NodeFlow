
"""
Created on Wed Aug 22 22:00:23 2018


TODO:
    
    
    
------
Each Network tracks all nodes & their connections - Animations/Edge Forces go here 
Each Node has a fn and has a list of terminals (shortcut to list of edges)
Each Terminal has list of edges "hooked" to` 
Each Edge knows From/To, Signal, and effect of edge (usually none if just transmission)
"""
import math

from PyQt5.QtWidgets import * #GUI (Graphical User Interface) library
from PyQt5 import QtGui, QtCore
#from pyqtgraph import flowchart
import numpy as np
import sys
from OHLib import * #@todo phase out reliance on OHL


import Window
import Objects
import Nodes
#@todo Options for frontend - 
#                   D3 - https://bl.ocks.org/mbostock/4566102
#                   React.js simulate https://github.com/esnet/react-network-diagrams
#                   Vue.js
#                   Bokeh? http://holoviews.org/reference/streams/bokeh/BoxEdit.html  
                    #       http://holoviews.org/user_guide/Network_Graphs.html
#                   QT
#@todo implement a "pluginfinder" thing
frontends={'QT'}#list of useable frontends only
def NodeFlowRun(frontend):
    #check if needs to load net 
    net=Objects.Network(nodes=Nodes)
    if frontend is not None:
        if frontend=='QT':
            qtwindowrun(net) #better suited as net method?
        elif frontend=='JS':
            #JSwindowrun(net)
            pass
    else:
        pass#run in headless mode
    
def qtwindowrun(net):
    app=0         
    #windthread=QtCore.QThread()
    
    app=QApplication(sys.argv)
    wind=Window.netWindow(net=net)
    app.exec_()
    
    
    