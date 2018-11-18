import datetime
###TUMBLR###
#theme color - #36465D
#https://www.tumblr.com/docs/npf
#                           /api
#justsomeantifas.com?
import pytumblr as tmblr
import pandas as pd
reqtokenURL='https://www.tumblr.com/oauth/request_token'
authURL='https://www.tumblr.com/oauth/authorize'
AccesstokenURL='https://www.tumblr.com/oauth/access_token'
myoauthkey='SJnqQLOsEiiQHo8JyjTpprFeTVXWt59ADdig8nBpNCJTzhg84L'
seckey='tgWUsCLHRhINeKSovlAeuoTguHCftkcLiwJnVQRzf2XHC2AVes'
client = tmblr.TumblrRestClient(myoauthkey,seckey)

class TumblrUser(object):
    def __init__(self,*args):
        self.uuid=uuid
        self.posts=dict()
    def addPost(self,Post):
        self.posts[Post.id]=Post
class TumblrPost(object):
    def __init__(self,postid,*args):
        self.id=postid
        
users=dict()
posts=dict()






def rbdfrompar(note,parent):#used in list comprehension
    #@todo better names
    if 'reblog_parent_blog_name' in note.keys():
        

        if note['reblog_parent_blog_name']==parent:
            return True
    
def filternotesbyparent(post,parent='justsomeantifas'):
    return [n for n in post['notes'] if rbdfrompar(n,parent)]

def splitnotesbytype(post):
    types={'reblog':[],'like':[],'reply':[]}

    for n in post['notes']:
        types[n['type']].append(n) 
    return types
def filtertags(posts,tags):
    pass
def getposts(user,before=None):
        if before is None:
            before=datetime.datetime.now().timestamp()
        posts=client.posts(user,notes_info=True)
        #@todo something to check if posts are already in list?
        return posts
def parseposts(posts):#passes in list of post objects with notes
    #['blog']['name']/['uuid']
    #TRAIL - who has left comments, returns reblog item
    pdposts=pd.DataFrame(posts)
    for post in posts:
         post
    pass

def buildNetwork(centeruser):
    
    
    
    pass





###TWITTER###



###FACEBOOK###
    

###DISCORD###
    #https://discordapp.com/developers/docs/intro
    ##7289DA