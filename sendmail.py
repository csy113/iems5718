import webapp2
from google.appengine.api import users
import event_func
import user_func
from google.appengine.api import mail
import logging

senderemail="iemscsy@gmail.com"
projectid="static-shine-554"

def sendImmediateEmail(eventid,eventname):
	logging.info("email test")
	userlist=event_func.getJoinedUserList(int(eventid))
	logging.info("sajnfewkfnw"+str(len(userlist)))
	for item in userlist:
			useremail=item.email
			message = mail.EmailMessage(sender=senderemail,
											subject="Event World: Your event is finalized!")

			message.to = useremail
			message.body = """
Dear """+ item.name + """:
The event owner has finalized the event--"""+eventname+""". Please check by the following link and attend the event in time.
"""+ """http://"""+projectid+""".appspot.com/event/view?eventid="""+str(eventid)+"""

Enjoy the event and have a good time.

Event World Team
"""
			message.send()



'''every item of updatelist is [eventid, eventname, [event update, new comment, new vote, cancelled]]'''
def sendEmail(updatelist, user, emailSubject):
	'''collect the update, create sendcontent'''
	updatecontent=["event update","new comment","new vote","cancelled"]
	sendcontent="""Some event update informations are lsited below:

"""
	for item in updatelist:
		count=1
		sendcontent=sendcontent+"Event: "+item[1]+" has "
		for index in range(len(item[2])):
				if item[2][index]==1:
						sendcontent=sendcontent+str(count)+""".  """+updatecontent[index] + ' '
						count=count+1
		sendcontent=sendcontent+"""
Please click the link http://"""+projectid+""".appspot.com/event/view?eventid=%d to see details.
            
""" % item[0]
     
            
		useremail=user.email
		message = mail.EmailMessage(sender=senderemail,
												subject=emailSubject)

		message.to = useremail
		message.body = """
Dear """+ user.name +""" :
"""+sendcontent+"""
Please let us know if you have any questions.

Event World Team
"""
		message.send()

