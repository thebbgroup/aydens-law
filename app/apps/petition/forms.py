from flask.ext.wtf import Form, BooleanField, TextField
from flask.ext.wtf.html5 import DateField, EmailField
from wtforms.validators import Required

from .models import Signature


class PetitionForm(Form):
    name = TextField('Name', validators=[Required()])
    email = EmailField('Email', validators=[Required()])
    dob = DateField('Date of Birth', validators=[Required()])
    address = TextField('Address')
    town = TextField('Town / City')
    postcode = TextField('Postcode')
    country = TextField('Country')
    opt_out = BooleanField('Keep me updated about Ayden\'s Law', default=True)
