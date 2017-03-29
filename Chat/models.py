from google.appengine.ext import ndb

class Message(ndb.Model):
    nickname = ndb.StringProperty()
    message = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
