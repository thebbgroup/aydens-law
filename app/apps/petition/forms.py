import re

from flask.ext.wtf import Form, BooleanField, TextField
from flask.ext.wtf.html5 import DateField, EmailField
from wtforms.validators import Email, Required, ValidationError

from .models import Signature


dob_regex = re.compile(r'(0[1-9]|1\d|2\d|3[01]).*(0[1-9]|1[012]).*(19\d{2}|200\d|201[0-3])')

class PetitionForm(Form):
    name = TextField('Name', validators=[Required()])
    email = EmailField('Email', validators=[Required(), Email()])
    dob = TextField('Date of Birth (DD/MM/YYYY)', validators=[Required()])
    address = TextField('Address')
    town = TextField('Town / City')
    postcode = TextField('Postcode')
    country = TextField('Country')
    opt_out = BooleanField('Keep me updated about Ayden\'s Law', default=True)

    def validate_dob(form, field):
        if not dob_regex.match(field.data):
            raise ValidationError('Please enter your date of birth DD/MM/YYYY format')
