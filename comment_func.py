from google.appengine.ext import ndb    
from time_func import datetime2str
from django.utils.html import strip_tags

class Comment(ndb.Model):
	user = ndb.UserProperty(auto_current_user=True)
	content = ndb.TextProperty()
	time = ndb.DateTimeProperty(auto_now_add=True)
	eventid = ndb.StringProperty()

def addComment(eventid, content):
	comment = Comment(eventid=eventid,content=strip_tags(content))
	comment.put()
"""
        flag=0
        if len(eventidlist)==0:
            eventidlist.append(eventid)
        else:
            for i in eventidlist:
                if i==eventid:
                    flag=1
                    break
        if flag==0:
            eventidlist.append(eventid)
"""

def getCommentList(eid):
	que = Comment.query(Comment.eventid==eid).order(-Comment.time)
	result = que.fetch()
	commentlist=[]
	for item in result:
		commentlist.append([item.user.nickname(), item.content, datetime2str(item.time)])
	return commentlist

