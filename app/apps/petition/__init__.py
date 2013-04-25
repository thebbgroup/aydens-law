from flask import Blueprint, render_template, request

from app import app

from .forms import PetitionForm
from .models import Signature


petition_app = Blueprint('petition', __name__, template_folder='templates')

@petition_app.route('/')
def sign():
    form = PetitionForm()
    if form.validate_on_submit():
        sig = Signature(**form.data)
        sig.put()
        return redirect(url_for('petition.thanks'))
    return render_template('petition.jinja', form=form)

@petition_app.route('/thanks')
def thanks():
    return render_template('thanks.jinja')
