from flask import request
from google.appengine.ext import db

from app import config


if config['CACHE_BACKEND'] == 'memcached':
    from werkzeug.contrib.cache import MemcachedCache
    cache = MemcachedCache(['127.0.0.1:11211'])
elif config['CACHE_BACKEND'] == 'gae':
    from werkzeug.contrib.cache import GAEMemcachedCache
    cache = GAEMemcachedCache()
else:
    from werkzeug.contrib.cache import SimpleCache
    cache = SimpleCache()


class Signature(db.Model):
    name = db.StringProperty(required=True)
    email = db.StringProperty(required=True)
    dob = db.DateProperty()
    ip = db.StringProperty()
    address = db.StringProperty()
    town = db.StringProperty()
    postcode = db.StringProperty()
    country = db.StringProperty()
    opt_out = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        kwargs['ip'] = request.remote_addr
        super(Signature, self).__init__(*args, **kwargs)

    @staticmethod
    def recent():
        sigs = memcache.get('recent-sigs')
        if sigs is None:
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

        return found_in(mc) or found_in(db)

    def save(self):

        # prevent duplicate signatures
        if not self.exists():
            self.put()

            # we don't care that this might not match the db
            first_nine = Signature.recent()[:9]
            memcache.set('recent-sigs', [self.name] + first_nine, 3600)

        # cache for 5 mins to avoid hitting the DB on repeated signing
        memcache.set(self.email, True, 300)
