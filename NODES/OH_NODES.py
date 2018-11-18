__version__='0.0.1'
__meta__={'name':"Opportunity House Nodes",}
__required__={'HV'}
__optional__={'Panel','Django','Socmedia'}

try: 
    from HV_NODES import *
    #@todo have a boundingregion for relevant data from some other dataset
    
    def schedboxes(emps,workday=None,daywindow=(8,20),colmap='Category10'):#@todo better names
        bxs=[]
        teams=dict()
        #@todo more robust datetime axis thing 
        #@todo dropdown to change colormap
        #@todo colormap labels show team name/some workaround
        
#        http://holoviews.org/reference/elements/bokeh/Polygons.html
        for e in range(len(emps)):#@todo dropdown panel box for how employee order is sorted
            #@todo optional single day/multi-day
            d=0
            for s in list(emps.values())[e].shifts.values():
#                s=list(emps.values())[e].shifts[workday]
                
                if s.time is not None:
                    #@todo make more robust than hour
                    midshift=(sum(t.hour for t in s.time))/2
                    shiftlen=abs((s.time[1]-s.time[0]).total_seconds())/(60*24)
                    
                    employeeheight=1
                    employeeloc=e
#                    print(midshift,employeeloc,(shiftlen,employeeheight))
                    if s.team in teams.keys():
                        tm=teams[s.team]
                    else:
                        tm=len(teams)+1
                        teams[s.team]=tm
#                    print(tm)
                    bxs.append({('x','y'):hv.Box(d+midshift,employeeloc,(shiftlen,employeeheight)).array(),'team':tm})
                    
                d=d+24#@todo phase this out thru proper timestamps
                    
        return hv.Polygons(bxs,vdims='team').options(colorbar=True,yaxis=None,cmap=colmap)
    def donspikes(dons,wrapweek=True):
        if wrapweek:#modulo, best used as fed into rolling average window
            pass
        
        
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
except:
    print('eror')