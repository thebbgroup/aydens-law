from flask import Blueprint, Response, render_template, request, redirect, url_for
from functools import wraps

from app import app

from .forms import PetitionForm
from .models import Signature


petition_app = Blueprint('petition', __name__, template_folder='templates')

@petition_app.route('/', methods=['GET', 'POST'])
def sign():
    form = PetitionForm()

    if form.validate_on_submit():
        Signature(**form.data).save()
        return redirect(url_for('petition.thanks'))

    return render_template('petition.jinja', form=form, sigs=Signature.recent())

@petition_app.route('/thanks')
def thanks():
    return render_template('thanks.jinja')

def check_auth(username, password):
    return username in app.config['AUTH_USERS'] and password == app.config['AUTH_USERS'][username]

def authenticate():
    return Response('Unauthorized', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
