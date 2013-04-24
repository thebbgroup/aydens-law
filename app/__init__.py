from flask import Flask, render_template


app = Flask('aydens-law')
app.config.from_object('app.settings')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.jinja'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.jinja'), 500

import views

from apps.petition import petition_app
app.register_blueprint(petition_app, url_prefix='/petition')
