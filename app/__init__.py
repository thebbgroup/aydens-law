from flask import Flask, render_template
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('app.settings')

db = SQLAlchemy(app)

mail = Mail(app)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.jinja'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.jinja'), 500

import views

from apps.petition import petition_app
app.register_blueprint(petition_app, url_prefix='/petition')

from apps.your_story import your_story_app
app.register_blueprint(your_story_app, url_prefix='/your-story')
