from google.appengine.ext import ndb

class Movie(ndb.Model):
    title = ndb.StringProperty()
    cover = ndb.StringProperty()
    rate = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)
