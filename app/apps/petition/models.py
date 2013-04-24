from google.appengine.ext import db


class Signature(db.Model):
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    dob = db.DateProperty()
    created = db.DateTimeProperty()
