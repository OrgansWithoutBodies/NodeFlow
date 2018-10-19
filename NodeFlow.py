
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
from OHLib import *


import Window
import Objects
import Nodes
#@todo Options for frontend - React.js/Qt https://github.com/esnet/react-network-diagrams

def NodeFlowRun(headless=False):#headless terminology confusing?
    #chocjs if needs to load net 
    net=Objects.Network(nodes=Nodes)
    if not headless:
        windowrun(net) #better suited as net method?
    
    
def windowrun(net):
    app=0         
    #windthread=QtCore.QThread()
    
    app=QApplication(sys.argv)
    wind=Window.netWindow(net=net)
    app.exec_()
    
    
    