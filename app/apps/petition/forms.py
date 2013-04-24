from flask.ext.wtf import Form, TextField
from wtforms.validators import Required

from .models import Signature


class PetitionForm(Form):
    name = TextField('Name', validators=[Required()])
    email = TextField('Email', validators=[Required()])
