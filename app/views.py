from flask import render_template

from app import app


@app.route('/')
def index():
    return render_template('index.jinja')

@app.route('/letter-to-pm')
def letter():
    return render_template('letter_to_pm.jinja')
