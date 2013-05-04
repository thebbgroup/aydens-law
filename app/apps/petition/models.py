from flask import request

from app import config, db


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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    dob = db.Column(db.Date)
    ip = db.Column(db.String(16))
    address = db.Column(db.String(200))
    town = db.Column(db.String(50))
    postcode = db.Column(db.String(20))
    country = db.Column(db.String(50))
    opt_out = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, *args, **kwargs):
        kwargs['ip'] = request.remote_addr
        super(Signature, self).__init__(*args, **kwargs)

    @staticmethod
    def recent():
        sigs = memcache.get('recent-sigs')
        if sigs is None:
            sigs = Signature.query.order_by(Signature.created)[:10]
            sigs = [sig.name for sig in sigs]
            memcache.set('recent-sigs', sigs, 3600)
        return sigs

    def exists(self):
        email = self.email
        mc = lambda: memcache.get(email)
        db = lambda: Signature.query.filter(Signature.email == email).count() > 0

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
            db.session.add(self)
            db.session.commit()

            # we don't care that this might not match the db
            first_nine = Signature.recent()[:9]
            memcache.set('recent-sigs', [self.name] + first_nine, 3600)

        # cache for 5 mins to avoid hitting the DB on repeated signing
        memcache.set(self.email, True, 300)
