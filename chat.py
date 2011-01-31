from google.appengine.api import xmpp
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Activity(db.Model):
    user = db.IMProperty()
    summary = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class XMPPHandler(webapp.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        cmd = message.body[0:5].lower()
        if cmd == "/help":
            message.reply = """
            Supported commands are:
            */help* (this help msg)
            """
        else:
            activity = Activity(user = db.IM("xmpp", message.sender), 
                                    summary = message.body)
            activity.put()
            message.reply("recorded")

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('deployFX')

        application = webapp.WSGIApplication(
        [('/', MainPage),
        ('/_ah/xmpp/message/chat/', XMPPHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()