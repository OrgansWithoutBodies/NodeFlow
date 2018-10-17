# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 14:35:30 2018

@author: V
"""
import holoviews as hv
import numpy as np
import pandas as pd
import sqlite3 as sql
from OHLib import Timer
#inputs of base dims & extra (manipulable) dims - dropdown for which sorta plot
#Spike Train  -  http://holoviews.org/user_guide/Customizing_Plots.html
#dashboard info - http://dev.holoviews.org/user_guide/Dashboards.html
#overlay&Holomap - http://holoviews.org/user_guide/Building_Composite_Objects.html
#%opts Curve
#whoops mosta this is unnecessary
#table.to.curve takes 5:39 for whole table, renderer save takes forever
#@todo able to choose between holomap (long wait upfront w big data) or dynamicmap (longish wait during render)
def timerange(NInit,NLast,NStep):
    ts=dict()
    for n in range(NInit,NLast,NStep):
        ts[n]=timegraph(n,['date','item'],['donor','amt'],['amt'],graphtype=hv.Scatter)
    return ts
def timegraph(N,basedims,sliderdims,overlaydims=None,tooltipdims=None,**kw):
    t=Timer()
    makehv(basedims=basedims,sliderdims=sliderdims,overlaydims=overlaydims,tooltipdims=tooltipdims,N=N,**kw)
    return(t.lap())
    
path=r'C:\Users\V\Python\Opphouse\Data\donations.db'
graphpath=r'C:\Users\V\Python\Opphouse\Projects\Website\opphouse\webapp\graphs'
def makehv(basedims,sliderdims=None,overlaydims=None,tooltipdims=None,graphtype=hv.Scatter,rendertype='bokeh',N=-1):
    #@todo flesh out so this is all that needs to be specified
    data=sql.connect(path).execute("SELECT donationid,categoryid,quantity,donorid,timestamp,firstname,lastname FROM DONATIONLINES JOIN DONORS ON DONATIONS.DONORID=DONORS.ID JOIN DONATIONS ON DONATIONLINES.DONATIONID=DONATIONS.ID").fetchall()
#    print(len(data))
    d=pd.DataFrame(data[0:N],columns=['donation','item','amt','donor','date','first','last']) #handle base data
    dims={'donor':hv.Dimension('donor',label='Donor ID',unit=''),#dimensions dictionary - used as basis for dict info, base unit for information of keys?
          'item':hv.Dimension('item',label='Item ID',unit=''),
          'amt':hv.Dimension('amt',label='Amount of item', unit='x'),
          'date':hv.Dimension('date',label='Date of Donation',unit=''),
          'donation':hv.Dimension('donation',label='Donation ID',unit=''),
          'last':hv.Dimension('last',label='Lastname',unit='')}
#default do overlaydims as 2nd level keys? bad idea maybe?
#@todo make base unit just str dict? create dims from it 
#@todo no need to repeat here dry
    #@todo need good way of realizing how to include info from foreign key stuff
#@todo measure O() values based on increased tablesize/slidersize/etc
    #holomap[sliderval] = overlay
    def slicedata(fdict=None,overlaydims=None):#gets relevant slice of data, used to figure out which plots get shown for multidimensional graphs
#    for 
        flist=list(fdict.keys())
    #    print(flist)
        truth=1
        for i in range(len(flist)):
            truth=(truth) & (d[flist[i]]==fdict[flist[i]])
        sdata=d[truth]
    #    print(len(sdata))
        return graphtype(sdata,basedims[0],basedims[1])#return limited sdata and use basedims

    def fs(label=None):#f's function - gets all the individual values to iterate through for dimensions which will be sliders
        return d[label].unique()
#@todo make hvdict flexible for variable length
        #@todo have some way of catching overdrawn memory and stopping/warning ahead of time
        #{(f1,f2,f3,...,fN):f(sliderdims[1]:f1,...,sliderdims[N]:fN) for fN in fs(sliderdims[N]) for N in len(sliderdims)}
        #EXPONENTIAL SCALING BASED ON N - careful!!!!
        #for each value in each sliderdim, there's an overlay
        #returns a dictionary whose key is a N-tuple (N=len(sliderdims)), andw whose values are hv graphs returned from slicedata for specific key
    hvdict={(f1,f2):slicedata({sliderdims[0]:f1,sliderdims[1]:f2}) for f1 in fs(sliderdims[0]) for f2 in fs(sliderdims[1])}

    kdims=[dims[i] for i in sliderdims]#slider names - don't actually affect what sliders do, but affects what it says
    h=hv.HoloMap(hvdict,kdims)#how holoview is handled - have other attributes like color/style etc
  
#    
#    if overlaydims is not None:#overlay must be in kdims
##        %%opts NdOverlay [width=600 legend_position='right']
##        print(fs(overlaydims[0]))
#        h.overlay(dims['amt'])
    #option to change view to table 
   #mode='server' #in renderer instance
#   @todo tweak changeable rendertype for if outputting to webserver (bokeh) or qt (matplotlib)
    if  rendertype=='bokeh':
        hv.renderer(rendertype).save(h,graphpath+r'\test')
    elif rendertype=='matplotlib':
        pass#just return a png/pdf/smth
    