import webapp2
import requests
from requests_toolbelt.adapters import appengine


class SendEmail(webapp2.RequestHandler):
    def post(self):
        requests.post(
            "https://api.mailgun.net/v3/sandboxf69711266f1e4f3fa5782627f0edccf8.mailgun.org/messages",
            auth=("api", "d5dd6bdd709ceec36eb7180f6ce7377d-52cbfb43-79c6b6b8"),
            data={"from": "Mailgun Sandbox <postmaster@sandboxf69711266f1e4f3fa5782627f0edccf8.mailgun.org>",
                  "to": "Wojciech Jarmakowski <s15983@pjwstk.edu.pl>",
                  "subject": "Hello",
                  "text": "Congratulations you just sent an email with Mailgun using task queue!  You are truly awesome!"})
        self.response.write('ok')


appengine.monkeypatch()
app = webapp2.WSGIApplication([
    ('/send', SendEmail)
], debug=True)
