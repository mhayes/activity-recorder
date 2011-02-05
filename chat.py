import logging
from google.appengine.ext import db
from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import xmpp_handlers

# Potential error messages that can be displayed
ERROR_SAVING= "An error preventing me from saving your activity"
ERROR_UNAUTHORIZED = "You're not allowed to do that"
ERROR_UNKNOWN_ID = "I can't seem to locate that record"

class Activity(db.Model):
    user = db.IMProperty()
    summary = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class XMPPHandler(xmpp_handlers.CommandHandler):
    def rpt_command(self, message=None):
        """Generate summary of activity."""
        im_from = db.IM("xmpp", message.sender)
        message.reply("Right away, check your e-mail in just a minute")
    def rm_command(self, message=None):
        """Removes user activity."""
        im_from = db.IM("xmpp", message.sender)
        activity_id = int(message.arg)
        activity = Activity.get_by_id(activity_id)
        if activity and activity.user == im_from:
            activity.delete()
            message.reply("That activity (%d) is gone!" % activity_id)
        elif activity and activity.user != im_from:
            message.reply(ERROR_UNAUTHORIZED)
        else:
            message.reply(ERROR_UNKNOWN_ID)
    def text_message(self, message=None):
        """Record activity."""
        im_from = db.IM("xmpp", message.sender)
        activity = Activity(user=im_from, summary=message.body)
        try:
            key = activity.put()
            message.reply("Logged as %s" % key.id())
        except:
            message.reply(ERROR_SAVING_MSG)

application = webapp.WSGIApplication(
    [('/_ah/xmpp/message/chat/', XMPPHandler)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()