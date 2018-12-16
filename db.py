from google.appengine.ext import ndb
import json


class UserTest(ndb.Model):
  username = ndb.StringProperty()
  password = ndb.StringProperty()
    
class Message(ndb.Model):
  text = ndb.StringProperty()
  msg = ndb.StringProperty()
	
def postMessage(data, content):
  message = Message()
  message.text = str(data)
  message.msg = str(content)
  key = message.put()
  id = key.id()
  return id
    
def postUser():
  user = UserTest()
  user.username = "Adam22"
  user.password = 'admin'
  key = user.put()
  id = key.id()
  return {'username': user.username, 'id': id}
    