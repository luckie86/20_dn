from google.appengine.ext import ndb


class Task(ndb.Model):
    task = ndb.StringProperty()
    status = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)