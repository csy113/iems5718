import webapp2
import event_func
import user_func
import session
from google.appengine.api import users

import os
# import module for templates
import jinja2
# for logging message to server log
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class HomePage(webapp2.RequestHandler):
	def get(self):
		user = user_func.getCurrentUser()
		userlist = user_func.getUserNameList()
		eventlist = event_func.getEventList()
		template_values = {
			'logoutlink' : '/logout',
			'csrftoken' : session.getOrInsertCSRFToken(self).token,
			'user' : user,
			'userlist' : userlist,
			'eventlist' : eventlist
		}
		template = JINJA_ENVIRONMENT.get_template('/template/mainPage.html')
		self.response.write(template.render(template_values))

class JoinedEventPage(webapp2.RequestHandler):
	def get(self):
		user = user_func.getCurrentUser()
		userlist = user_func.getUserNameList()
		eventlist = event_func.getEventListByVoter(user.user_id())
		template_values = {
			'logoutlink' : '/logout',
			'csrftoken' : session.getOrInsertCSRFToken(self).token,
			'userlist' : userlist,
			'user' : user,
			'eventlist' : eventlist
		}
		template = JINJA_ENVIRONMENT.get_template('/template/joined.html')
		self.response.write(template.render(template_values))

class MyEventPage(webapp2.RequestHandler):
	def get(self):
		user = user_func.getCurrentUser()
		userlist = user_func.getUserNameList()
		eventlist = event_func.getEventListByOwner(user.user_id())
		template_values = {
			'logoutlink' : '/logout',
			'csrftoken' : session.getOrInsertCSRFToken(self).token,
			'userlist' : userlist,
			'user' : user,
			'eventlist' : eventlist
		}
		template = JINJA_ENVIRONMENT.get_template('/template/myEvent.html')
		self.response.write(template.render(template_values))

        
app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/home', HomePage),
    ('/home/joinedeventlist', JoinedEventPage),
    ('/home/myeventlist', MyEventPage)
    ], debug=False)
