__version__='0.0.2'
"""
DONE:
0.
    0.2:    started logging
            Handles weeks ok
            Histogram works, want to be able to overlay
            default data connected to right sql keys
FUTURE GOALS
    ~0.3:   make weeks connect more easily
    ~0.5:   Flexible SQL keys
            get datashader working flexibly
            check datetype?
    1.0:    get nodes implemented right
default layouts - ():[]:{}:||
    ~#NAME#Graphtype(x,y,...):[sliders]:{overlay}:|Adjoints| fn $VAR$ --comment~
    Donations:
        Scatter(date,donor):[Item]:{Amount}
        #APW#Curve/{Stacked}Bar(day of week,amount):[Week]:{Item}  --average per weekday
        Curve/{Stacked}Bar(day of week,amount):{Item}-$APW$ --difference from average
        Curve():|Spike(time of day,donations)|
        #CATMAPSANKEY#Sankey(Catmap->DonationCategory,Amount) --can't include nodes w 0, initial node name must be different from terminal node name

    Transactions:
        Scatter():[]:{}
        
    """
import holoviews as hv
import numpy as np
import pandas as pd
import sqlite3 as sql
from OHLib import Timer

from bokeh.server.server import Server as bkserve
from bokeh.models import HoverTool

from holoviews.operation.datashader import datashade

from Objects import Node
#Stacked Curves -  hv.Area.stack(overlay) http://holoviews.org/reference/elements/matplotlib/Area.html
#base tutorial - http://pyviz.org/tutorial/
#datashader - http://datashader.org/getting_started/2_Pipeline.html
#inputs of base dims & extra (manipulable) dims - dropdown for which sorta plot
#Spike Train  -  http://holoviews.org/user_guide/Customizing_Plots.html
#dashboard info - http://dev.holoviews.org/user_guide/Dashboards.html
#overlay&Holomap - http://holoviews.org/user_guide/Building_Composite_Objects.html

#@todo able to choose between holomap (long wait upfront w big data) or dynamicmap (longish wait during )
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
def timerange(NInit,NLast,NStep):
    ts=dict()
    for n in range(NInit,NLast,NStep):
        ts[n]=timegraph(n,['date','item'],['donor','amt'],['amt'],graphtype=hv.Scatter)
    return ts
def timegraph(N,basedims,sliderdims,overlaydims=None,tooltipdims=None,**kw):
    t=Timer()
    makehv(basedims=basedims,sliderdims=sliderdims,overlaydims=overlaydims,tooltipdims=tooltipdims,N=N,**kw)
    return(t.lap())
    
    
    
    
def defaultgraphs():
    #@todo have way of getting all in same instance 
    #@todo improve loadtime - 16 secs on my laptop
    d=getdata(-1,True)
    tbl=hv.Table(getweekday(d))
    
    HVServer(tbl.to.bars(['weekday','item'],['value']))#@todo have better way of doing this
    makehv(data=weeklyitembrkdwn(d),basedims=['week','value'],sliderdims=['item'],overlaydims=['item'],server=True,graphtype=hv.Curve) #sum of item amts per week
    HVServer(catmapsankey(perc=True))
def catmapsankey(N=-1,perc=False):
    d=getdata(N,mapcats=False)      
    tperc=sum(d['amt']) if perc else 1#if perc then ends up dividing edge values by total else divides by 1
    map=sql.connect(path).execute("SELECT categorymap.name,donationcategories.name FROM CATEGORYMAP JOIN DONATIONCATEGORIES ON CATEGORYMAP.MAPSTOID=DONATIONCATEGORIES.ID").fetchall()
    mm=[['Original Category: '+m[0],'New Category: '+m[1],sum(d['amt'][d['item']==m[0]])/tperc]for m in map if sum(d['amt'][d['item']==m[0]])>0 ]
    return hv.Sankey(mm)
def weeklyitembrkdwn(d=None):
    if d is None:
        d=getdata(-1,True)
    t=groupbyweek(d,tidy=True)
    t.rename(columns={'date':'week'},inplace=True)
#    makehv(data=weeklyitembrkdwn(),basedims=['date','value'],sliderdims=['item'],overlaydims=['item'],server=True,graphtype=hv.Curve)
    return t
def getweekday(d,dkey='date',vkey='amt',itmkey='item'):#@todo have simple way of deciding startday
    #@todo some way of easily doing weighted sum
    d[dkey]=pd.to_datetime(d[dkey])
    d['weekday']=d[dkey].apply(lambda x: x.strftime("%w - %A"))
    ds=d.groupby(['weekday',itmkey]).sum()
    md=meltweek(ds[vkey].unstack(1),'weekday')
    return md

   #@todo some way to mark date column
   #dkey - column name of date, kkey - what to group by, vkey - column to weigh kkey, startkey - 'W','W-SUN','W-MON' - how week starts, fn - how group is aggregated
def groupbyweek(d,dkey='date',kkey='item',vkey='amt',startkey='W-SUN',fn=sum,tidy=False):#fits better somewhere else?
    d[dkey]=pd.to_datetime(d[dkey])
    d.groupby([pd.Grouper(key=dkey,freq=startkey)])
#    
#    if  pd.core.dtypes.dtypes.DatetimeTZDtype not in d.dtypes.values:#checks which values are datetimes
#        d[dkey]=pd.to_datetime(d[dkey])
#        print(d)
    td=(d.groupby(kkey)                
    .apply(lambda g:               # work on groups of col1
        g.set_index(dkey)        
        [[vkey]]
        .resample(startkey,how=fn)  # sum the amount field across weeks - @todo update 
    )
    .unstack(level=0)              # pivot the col1 index rows to columns
    .fillna(0)
)
    if tidy:#if wanna make sql-friendly 
        print(td.keys())
        return meltweek(td[vkey])
    else:
        return td
def meltweek(d,dkey='date'):
    if dkey not in d.columns:
        d[dkey]=d.index
    m=pd.melt(d,dkey)
    if dkey=='date':
        m[dkey]=m[dkey].dt.strftime('%x')
    return m

def getdata(N=-1,mapcats=True,nameformat="lastname||', '||firstname"):
    maps={False:['categorymap.name'," JOIN CATEGORYMAP ON DONATIONLINES.CATEGORYID=CATEGORYMAP.ID"],#@todo make less janky
          True:['donationcategories.name',' JOIN DONATIONCATEGORIES ON CATEGORYMAP.MAPSTOID=DONATIONCATEGORIES.ID']}
    sqlquery="""
                    SELECT donationid,{0},quantity,timestamp, {1}  
                        FROM DONATIONLINES 
                            JOIN DONORS ON DONATIONS.DONORID=DONORS.ID 
                            JOIN DONATIONS ON DONATIONLINES.DONATIONID=DONATIONS.ID
                            JOIN CATEGORYMAP ON DONATIONLINES.CATEGORYID=CATEGORYMAP.ID""".format(maps[mapcats][0],nameformat)
    if mapcats:
        sqlquery=sqlquery+""" JOIN DONATIONCATEGORIES ON CATEGORYMAP.MAPSTOID=DONATIONCATEGORIES.ID"""
    data=sql.connect(path).execute(sqlquery).fetchall()
#    print(len(data))
#    [0:N]
    
    d=pd.DataFrame(data[0:N],columns=['donation','item','amt','date','donor']) #handle base data
    return d
path=r'C:\Users\V\Python\Opphouse\Data\donations.db'
graphpath=r'C:\Users\V\Python\Opphouse\Projects\Website\opphouse\webapp\graphs'
def makehv(basedims,data=None,sliderdims=None,overlaydims=None,histdims=None,tooltipdims=None,dshade=False,graphtype=hv.Scatter,rendertype='bokeh',N=-1,server=False,adj=None,sz=(1000,500)):
    #@todo have adjoin choices clear
    hv.extension(rendertype)
    #@todo optional if maps to base categories or categorymap
    #@todo customizable name format
    if data is None:
        d=getdata(N)
    else:d=data
    dims={'donor':hv.Dimension('donor',label='Donor ID',unit=''),#dimensions dictionary - used as basis for dict info, base unit for information of keys?
          'item':hv.Dimension('item',label='Item ID',unit=''),
          'amt':hv.Dimension('amt',label='Amount of item', unit='x'),
          'date':hv.Dimension('date',label='Date of Donation',unit=''),
          'donation':hv.Dimension('donation',label='Donation ID',unit='')}
#default do overlaydims as 2nd level keys? bad idea maybe?
#@todo make base unit just str dict? create dims from it 
#@todo no need to repeat here dry
    #@todo need good way of realizing how to include info from foreign key stuff
    #@todo measure O() values based on increased tablesize/slidersize/etc
    #@todo have some way of connecting key names to id
    """
    Slide/Animate through{
        Overlays of {
            Decorated{Base Plots}
            }
        }
    """
        #@todo have some way of catching overdrawn memory and stopping/warning ahead of time
 
       #for each value in each sliderdim, there's an overlay
    if type(d)==pd.DataFrame:#@todo make more robust 
        tbl=hv.Dataset(d)
#        vdims=list(set(sliderdims).union(set(histdims)).union(set(overlaydims)))
#        print(vdims)
        h=hv.HoloMap(tbl.to(graphtype,kdims=basedims,vdims=sliderdims,groupby=sliderdims))
##        print(h.keys())
        if dshade:
            h=datashade(h)
        if overlaydims is not None:
            h=h.overlay(overlaydims)
        if histdims is not None: 
            h1=hv.operation.histogram(h,num_bins=50,dimension=histdims[0],mean_weighted=False)
            h=h<<h1
#        h.groupby(['amt']).hist(num_bins=100,dimension=[basedims[0]],mean_weighted=True)
#        h=h.collate()
#   #@todo implement datashade, prompt user if trying to show too big of data
        
#        if overlaydims is not None:
#            h=h*h.overlay(overlaydims)#overlaydims must be in sliderdims - @todo better name
#@todo make histogram bin number automatic default/settable
##        if hist:ration.histogram(h,num_bins=100,dimension=basedims[0],mean_weighted=True)
        #@todo easy way to include sums etc
#        h1.overlay(overlaydims)
#             h=h<<h1
        finalh=h
    else:
        hvdict={(f1,f2):slicedata({sliderdims[0]:f1,sliderdims[1]:f2}) for f1 in fs(sliderdims[0]) for f2 in fs(sliderdims[1])}

        h=hv.DynamicMap(hvdict,kdims)#how holoview is handled - have other attributes like color/style etc
    
#    hover=HoverTool(tooltips=[(t,'$'+str(t)) for t in tooltipdims])
    hover=HoverTool(tooltips=[("test","$index"),])
#    print(hover)
    
    #options
    #@todo have better flexible way of doing styles
    hv.util.opts(graphtype.__name__+' [tools=["hover","lasso_select"] colorbar=True width={0} height={1}] (alpha=0.6,muted_alpha=0.01,size=5)'.format(sz[0],sz[1]))
#    hv.util.opts('Histogram (alpha=0.3)')
    
#    if overlaydims is not None:#overlay must be in kdims
##        %%opts NdOverlay [width=600 legend_position='right']
##        print(fs(overlaydims[0]))
#        h.overlay(dims['amt'])
    #option to change view to table 
   #mode='server' #in renderer instance
#   @todo tweak changeable rendertype for if outputting to webserver (bokeh) or qt (matplotlib)
    if server:
        HVServer(finalh,rendertype)
#        doc.title='test server'
    else:
        hv.renderer(rendertype).save(h,graphpath+r'\test')
#    elif rendertype=='matplotlib':
#        pass#just return a png/pdf/smth
#    
#makehv(['date','item'],['donor','amt'],['amt'],graphtype=hv.Points,server=True)

def HVServer(hvobj,rendertype='bokeh',instance=None):
    r=hv.renderer(rendertype)
#        r.get_plot(setattr(plot, 'plot_width', 1700)
#setattr(plot, 'plot_height', 900)
    doc=r.app(hvobj)
#        doc=r.server_doc(dh)
    doc.title='test'
    s=bkserve({'/':doc},port=0)
    s.start()
    s.show('/')


#HV NODES HERE 
#@todo optional background grid
#
class HVAdjoinNode(Node):
    pass
class HVGraphNode(Node):
    #inputs:
    pass
class HVOverlayNode(Node):#redundant - specified by graph?
    pass

class HVBokehServerNode(Node):#name too big?
    pass
class HVStyleNode(Node):
    def __init__(self,**kw):
        styledict={#available styles - @todo make sure each of these are integrated with & w/o values
                'renderer':None,#specify somewhere else?
                'width':None,
                'height':None,
                'alpha':None,
                'muted_alpha':None,
                'size':None,
                'colors':[],
                'shapes':[],#better as None?
                'cmap':None,
                }
#with a given dict of values