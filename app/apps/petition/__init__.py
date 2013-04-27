from flask import Blueprint, render_template, request, redirect, url_for

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
