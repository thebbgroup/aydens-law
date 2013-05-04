import app
from werkzeug import DebuggedApplication

if __name__ == '__main__':
    app.app.debug = True
    app.app = DebuggedApplication(app.app, evalex=True)
    app.app.app.run('localhost', 9000)
