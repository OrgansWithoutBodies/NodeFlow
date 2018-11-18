#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__version__="0.0.1"

__required__={}
__optional__={'PANEL','HV'}
"""
Created on Sun Nov  4 21:27:46 2018

@author: v
"""
import datetime as dt

import psutil
import holoviews as hv
import pandas as pd


try:    
    from PANEL_NODES import *
except:
    pass

#@todo able to define which stats to get
#@todo flexible callback times
#@todo make check if Holoviews/HV_NODES is installed/plugged-in, if not then only do psutil stuff
#@todo flexible way to get derivative
class Attribute(object):
    pass


hv.extension('bokeh',logo=False)

###HVS DEFINED### #@todo make dependent on presence of dependencies
def ATT_box(data,fade=False):
    #@todo have dots "fade over time" - order in list is tied to opacity
    #@todo option for arrow of d(whisker)/dt http://holoviews.org/reference/elements/bokeh/Arrow.html#bokeh-gallery-arrow
    #@todo option for fixed height plot
    pass
def ATT_stack(data,norm=False):
    pass
def ATT_curves(data,att):
    pass

def mem_stack(data):
    data = pd.melt(data, 'index', var_name='Type', value_name='Usage')
    areas = hv.Dataset(data).to(hv.Area, 'index', 'Usage')
    return hv.Area.stack(areas.overlay()).relabel('Memory')

def cpu_box(data,fade=False):
    
    return hv.BoxWhisker(data, 'CPU', 'Utilization').relabel('CPU Usage')

def cpu_curves(data):

#    ds=hv.Dataset(data)
#    crv=ds.to(hv.Curve,'time',"Utilization")
#    crv.overlay(['CPU'])
#    return crv.relabel('test')

    crvs=[hv.Curve(data[data['CPU']==i],'time','Utilization') for i in data['CPU'].values]
    return hv.Overlay(crvs)
def cpu_stack(data,norm=True):
    if norm:
        data['Utilization']=data['Utilization']/sum(data['Utilization'])*100
        
    areas = hv.Dataset(data).to(hv.Area, 'time', ['Utilization','CPU'],'CPU')
    return hv.Area.stack(areas.overlay()).relabel('CPU')

def net_stack(data,conn=True,io=True,metric='Megabytes'):#@todo different (multiple) graphs based on ATT options
    metrics={'Gigabytes':10**9,
             'Megabytes':10**6,
             'Kilobytes':10**3}
    data=data.loc[:,['time','brec','bsen']]
    
    data['brec']=data['brec']/(metrics[metric])
    data['bsen']=data['bsen']/(metrics[metric])
    vmet='Value '+metric
    data = pd.melt(data,'time', var_name='Type', value_name=vmet)
    areas = hv.Dataset(data).to(hv.Area, 'time', vmet)
    return hv.Area.stack(areas.overlay()).relabel('Network Traffic')
def dsk_pie(data,perdisk=False):
    if perdisk:
        pass
    else:
        pass
#def dsk_







##VARIABLES###
STRMS={'mem','cpu','net'}#controls which objects are shown @todo better nomenclature?
PERIOD=500#ms
ATTDICT={'mem':{'rng':'Utilization','grph':mem_stack},
      'cpu':{'rng':'Usage','grph':cpu_box},
      'net':{'rng':'Value','grph':net_stack},#not Value?
      'dsk':{'rng':'Utilization','grph':cpu_box},
      'sns':{'rng':'Value','grph':lambda data:ATT_curves(data,'sns')}}#total data dictionary


#@todo global buttons - purge cache button, period, dropdown of which attributes/options - all same stuff that NF nodes input 
#https://panel.pyviz.org/user_guide/Widgets.html 
#@todo bool fahrenheit vs. celsius
#@todo
def submitoptions():
    pass

###PANELS/OPTIONS####
if pn_available:
    PNLS=dict()#@todo connect these somehow?
    PNLS['attsel']=widgets.MultiSelect(options=list(ATTDICT.keys()),value=list(STRMS),name='Attribute Select')    
    PNLS['fahrsel']=widgets.Checkbox(name='Fahrenheit')
#    PNLS[]
    PNLS['submit']=widgets.Action(name="Submit options",button_type='danger')
    #@todo connect trigger/watchers - param.watch http://param.pyviz.org/Reference_Manual/param.html#param.parameterized.Parameters.trigger

    #[layoutobj].param.watch(testfn,'clicks')
def getpsutildoc(strms):#@todo make as wrapper fn for whole script
    pass


####GET DATAS####
def get_mem_data(swap=False):
    vmem = psutil.virtual_memory()
    t=pd.Timestamp.now()
    df = pd.DataFrame(dict(free=vmem.free/vmem.total,
                           used=vmem.used/vmem.total),
                      index=[t])
    if swap:
        df[t]['swap']=psutil.swap_memory().used
    return df*100

def get_cpu_data():
    cpu_percent = psutil.cpu_percent(percpu=True)
    df = pd.DataFrame(list(enumerate(cpu_percent)),
                      columns=['CPU', 'Utilization'])
    df['time'] = pd.Timestamp.now()
    return df

def get_net_data(conn=True,io=True):
    df=dict()
    t=pd.Timestamp.now()
    if conn:
        ncon=psutil.net_connections()
        df['nsoc']=len(ncon)#'Number of Open Sockets'
        #@todo 
    if io: 
        ctrs=psutil.net_io_counters()
        df['brec']=ctrs.bytes_recv#'Total Bytes Received'
        df['bsen']=ctrs.bytes_sent#Total Bytes Sent
        #@differentiate from last val somehow 
    df['time']=t
        
    return pd.DataFrame(df,index=[t])
def get_dsk_data(use=True,io=True,perdisk=False):
    df=dict()#@todo have perdisk toggleable option
    if perdisk:
        
        prts=psutil.disk_partitions()
        if use:
            df['usfre']=dict()
            df['usttl']=dict()
            for p in prts:
                usg=psutil.disk_usage(p.mountpoint)
                df['usfre'][p.mountpoint]=usg.free
                df['usttl'][p.mountpoint]=usg.total

        if io:
            disks=psutil.disk_io_counters(perdisk=perdisk)
            df['bwt']=dict()
            df['brd']=dict()
            for d in disks:
                df['bwt'][d]=disks[d].write_bytes
                df['brd'][d]=disks[d].read_bytes
        return df
    else:
        if io:
            ctrs=psutil.disk_io_counters()
            df['bwt']=ctrs.write_bytes
            df['brd']=ctrs.read_bytes
        return df
def get_sns_data(fan=True,bat=True,tem=True,fahrenheit=False):
    df=dict()
    if fan:
        fns=psutil.sensors_fans()
        df['fncur']=dict()
        for c in fns.keys():#each different system's fans
            for f in fns[c]:
                df['fncur'][f.label]=f.current
                
    if bat:
        btry=psutil.sensors_battery()
        df['btprc']=btry.percent
    if tem:#@todo have some way of linking CPU stats to coretemp? http://holoviews.org/user_guide/Custom_Interactivity.html#Linking-streams-to-plots
        tmps=psutil.sensors_temperatures(fahrenheit)
        df['tmp']=dict()
        for prb in tmps.keys():
            for itm in tmps[prb]:
                df['tmp'][prb+itm.label]=itm.current
                
        
    return df
def get_ATT_datas(ATTS):
    datafns={'mem':get_mem_data,
             'net':get_net_data,
             'dsk':get_dsk_data,
             'cpu':get_cpu_data,
             'sns':get_sns_data,
             }
    
    return {s:datafns[s] for s in ATTS}
DATAS=get_ATT_datas(STRMS)


#### Set up StreamingDataFrames and add async callback
def ATT_streams(ATTS={}):
    strms=dict()
    if 'cpu' in ATTS:
        strms['cpu']= hv.streams.Buffer(get_cpu_data(),800, index=False)
    if 'mem' in ATTS:
        strms['mem'] = hv.streams.Buffer(get_mem_data())
    if 'net' in ATTS:
        strms['net']=hv.streams.Buffer(get_net_data())
    if 'dsk' in ATTS:
        strms['dsk']=hv.streams.Buffer(get_dsk_data())
    return strms
STREAMOBJS=ATT_streams(STRMS)

def sendstreamsdata(atts,streamobjs,dataobjs):#@todo better name
    {streamobjs[a].send(dataobjs[a]()) for a in atts}


# Define DynamicMaps and display plot
def ATT_dmap(graph,stream):
    return hv.DynamicMap(graph,streams=[stream])
cpu_dmap = ATT_dmap(cpu_stack,STREAMOBJS['cpu'])

mem_dmap = ATT_dmap(mem_stack, STREAMOBJS['mem'])
#mem_dmap.periodic(0.05,100)
#@todo can have multiple graphs per att?
DMAPS={s:ATT_dmap(ATTDICT[s]['grph'],STREAMOBJS[s]) for s in STRMS}


#####OPTS#####
def ATT_opts(strms={}):
    opts=dict()
    for s in strms:#@todo check if forloop is more efficient than ifs - minimize checks whwile being generic
        if s=='cpu': 
            opts[s]= {'plot': dict(width=500, height=400, color_index='CPU'),
            'style': dict(box_fill_color=hv.Cycle('Category20'))}
        elif s=='mem':
             opts[s]={'plot':dict(height=400, width=400)}
        elif s=='net':
             opts[s]={'plot':dict(height=400, width=400)}
        elif s=='dsk':
             opts[s]={'plot':dict(height=400, width=400)}
    return opts
OPTS=ATT_opts(STRMS)

# Render plots and attach periodic callback
PLOT=[DMAPS[s].redim.range(**{ATTDICT[s]['rng']:(0,100)}).opts(**OPTS[s]) for s in STRMS]
FINPLOT=PLOT[0]#@todo less janky
if len(PLOT)>1:
    for p in PLOT[1:]:
        FINPLOT=FINPLOT+p
renderer = hv.renderer('bokeh')
doc=renderer.server_doc(FINPLOT)
#doc=renderer.server_doc(mem_dmap)

doc.add_periodic_callback(lambda:sendstreamsdata(STRMS,STREAMOBJS,DATAS), PERIOD)



###NODEFLOW STUFF###
def PSUTLAttributeNode():#
    pass
def PSUTLOptNode():
    pass#@todo select options such as - which graphs to choose (@todo able to be custom?)
def PSUTLStreamNode():
    pass#@todo make wrappers for HVStreamNodes