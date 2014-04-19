import webapp2
import event_func
import user_func
from sendmail import sendEmail
from google.appengine.api import users
from google.appengine.ext import ndb    

# for logging message to server log
import logging

class TestCounter(ndb.Model):
	count = ndb.IntegerProperty()
	updatedTime = ndb.DateTimeProperty(auto_now=True)

class TestReport(webapp2.RequestHandler):
	"""
	A test class for cron job
	"""
	def get(self):
		key = ndb.Key('TestCounter', '1')
		count = key.get()
		if count is None:
			count = TestCounter()
			count.key = key
			count.count = 1
		else:
			count.count = count.count + 1
		count.put()

class DailyReport(webapp2.RequestHandler):
	def get(self):
		userlist=user_func.getUserList()
		for user in userlist:
			updateownlist = event_func.getUpdatedEventListByOwner(user.key.id())
			sendEmail(updateownlist, user, "Event world: The events you created have update")
			updatevotelist = event_func.getUpdatedEventListByVoter(user.key.id())
			sendEmail(updatevotelist, user, "Event world: The events you joined have update")
        
app = webapp2.WSGIApplication([
    ('/report/test', TestReport),
    ('/report/dailyemail', DailyReport),
    ], debug=False)
