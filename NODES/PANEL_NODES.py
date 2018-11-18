#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 01:33:42 2018

@author: v
"""
__version__="0.0.0"

__required__={}
__optional__={}

try:
    import panel as pn
    from panel.interact import interact, interactive, fixed, interact_manual
    from panel import widgets
    from panel import layout
    pn_available=True
except:
    pn_available=False
    
    
def pnTableTab(tbl,graphtype,kdims,vdims,groupby):#@todo make dims not need to be inputted?
#def pnTableTab(tbl,grph,nm):
    #@todo make workable with streams  http://param.pyviz.org/Reference_Manual/param.html#param.parameterized.Parameters.set_dynamic_time_fn ?
    #@todo changeable table size?
    #@todo some sorta highlight from table vs. graph
    #@todo work out tabname dealio
        L=layout.Tabs((graphtype.__name__,hv.HoloMap(tbl.to(graphtype,kdims,vdims,groupby))),('Table',tbl))
#        L=layout.Tabs((nm,grph),('Table',tbl))  
        return L

