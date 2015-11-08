from google.appengine.ext import ndb


class BaseModel(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    modified = ndb.DateTimeProperty(auto_now=True)

    def delete(self):
        self.key.delete()

    @classmethod
    def all(cls):
        return cls.query()
