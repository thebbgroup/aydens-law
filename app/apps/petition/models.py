import logging
from google.appengine.api import memcache
from google.appengine.ext import db


class Signature(db.Model):
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    dob = db.DateProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def recent():
        sigs = memcache.get('recent-sigs')
        if sigs is None:
            logging.info('fetching recent sigs from db')
            sigs = Signature.all().order("-created").fetch(limit=10)
            sigs = [sig.name for sig in sigs]
            memcache.set('recent-sigs', sigs, 3600)
        return sigs

    def exists(self):
        email = self.email
        mc = lambda: memcache.get(email)
        db = lambda: Signature.all().filter("email =", email).count() > 0

        def found_in(search):
            found = search()
            if found:
                # cache for 5 mins to avoid hitting the DB on repeated signing
                memcache.set(email, True, 300)
            return found

        def log(x):
            logging.info('searching db')
            return x

        return found_in(mc) or log(found_in(db))

    def save(self):

        # prevent duplicate signatures
        if not self.exists():
            logging.info('inserting into db')
            self.put()

            # we don't care that this might not match the db
            first_nine = Signature.recent()[:9]
            memcache.set('recent-sigs', [self.name] + first_nine, 3600)

        # cache for 5 mins to avoid hitting the DB on repeated signing
        memcache.set(self.email, True, 300)
