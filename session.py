from google.appengine.ext import ndb    
from random import randrange
from google.appengine.api import users
import logging

class CSRFToken(ndb.Model):
	createTime = ndb.DateTimeProperty(auto_now_add=True)
	token = ndb.StringProperty()

def checkTokenValid(webapp2ReqHandle):
	try:
		sessionID = int(webapp2ReqHandle.request.cookies.get('sessionid'))
	except TypeError:
		sessionID = None
		ret = False
	else:
		csrfToken = webapp2ReqHandle.request.get('csrftoken')
		storedToken= ndb.Key('CSRFToken', sessionID).get()
		if storedToken is None:
			ret = False
		else:
			ret = (storedToken.token == csrfToken)

	if ret == False:
		logging.warn('CSRF Token [%s] is invalid' % csrfToken)
		return ret

def _setCookie(webapp2ReqHandle, sessionID):
#TODO add expire time
	webapp2ReqHandle.response.set_cookie('sessionid', '%d' % sessionID, httponly=True)

def _createCSRFToken():
	token = '%s' % randrange(1000, 99999999)
	csrfToken = CSRFToken(
		token=token)
	sessionID= csrfToken.put()
	logging.info('CSRF Token created')
	return csrfToken

def getCSRFToken(webapp2ReqHandle):
	try:
		sessionID = int(webapp2ReqHandle.request.cookies.get('sessionid'))
	except TypeError:
		csrfToken = None
	else:
		csrfToken = ndb.Key('CSRFToken', sessionID).get()
	return csrfToken
	
def getOrInsertCSRFToken(webapp2ReqHandle):
	csrfToken = getCSRFToken(webapp2ReqHandle)
	if csrfToken is None:
		csrfToken = _createCSRFToken()
		_setCookie(webapp2ReqHandle, csrfToken.key.id())
	logging.info('Token retrived: %s' % csrfToken)
	return csrfToken

def deleteCSRFToken(webapp2ReqHandle):
	try:
		sessionID = int(webapp2ReqHandle.request.cookies.get('sessionid'))
	except TypeError:
		pass
	else:
		ndb.Key('CSRFToken', sessionID).delete()
		webapp2ReqHandle.response.unset_cookie('sessionid')

