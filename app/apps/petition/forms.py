from datetime import date
import re

from flask.ext.wtf import Form, BooleanField, TextField
from flask.ext.wtf.html5 import DateField, EmailField
from wtforms.validators import Email, Required, ValidationError

from .models import Signature


dob_regex = re.compile(r'(0[1-9]|1\d|2\d|3[01]).*(0[1-9]|1[012]).*(19\d{2}|200\d|201[0-3])')

class DobField(TextField):
    def process_formdata(self, valuelist):
        if valuelist:
            m = dob_regex.match(valuelist[0])
            if m:
                day, month, year = m.groups()
                self.data = date(int(year), int(month), int(day))
            else:
                self.data = None
                raise ValueError(self.gettext('Not a valid date value'))


class PetitionForm(Form):
    name = TextField('Name', validators=[Required()])
    email = EmailField('Email', validators=[Required(), Email()])
    dob = DobField('Date of Birth (DD/MM/YYYY)', validators=[Required()])
    address = TextField('Address')
    town = TextField('Town / City')
    postcode = TextField('Postcode')
    country = TextField('Country')
    opt_out = BooleanField('Keep me updated about Ayden\'s Law', default=True)
