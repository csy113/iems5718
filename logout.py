import webapp2
from google.appengine.api import users
import session

import os
# import module for templates
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Logout(webapp2.RequestHandler):
	def get(self):
		session.deleteCSRFToken(self)
		self.redirect(users.create_logout_url('/'))

app = webapp2.WSGIApplication([
    ('/logout', Logout),
    ], debug=False)
