from google.appengine.ext import ndb
import json


class UserTest(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    
def postUser():
    user = UserTest()
    user.username = "Adam22"
    user.password = 'admin'
    key = user.put()
    id = key.id()
    return {'username': user.username, 'id': id}
    