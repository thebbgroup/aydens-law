import os
import sys

sys.path.append(os.path.join(os.path.abspath('.'), 'lib'))
import app

from werkzeug import DebuggedApplication

if app.app.config['DEBUG']:
    app.app.debug = True
    app.app = DebuggedApplication(app.app, evalex=True)
