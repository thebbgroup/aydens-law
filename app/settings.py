import os


DEBUG_MODE = False

if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    DEBUG_MODE = True

DEBUG = DEBUG_MODE

CACHE_BACKEND = memcached

SQLALCHEMY_DATABASE_URI = 'sqlite:///aydenslaw.db'

SECRET_KEY = '&\xfd\x10\x1b\xe8\xf1\xe0\xa8\xef\xf7\x1cN7o\xdc\xce \xbfV\xd2=:.\xe0\xdf\x94\xb34pER\xb5\xecL\xaf!\xd4\x00\x93\xc7,\xfcz\xd2d\x05\xfd7O\xd6\x08wR(*\xf3\x93\x97\xa6\xc6\xaaS\xf08'
