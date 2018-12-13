from google.appengine.ext import ndb


class User(ndb.Model):
    username = nbd.StringProperty();
    
def getUser(self, admin):
    user = User(username="adam")
    user.put()