from flask.ext.wtf import Form, TextAreaField, TextField
from flask.ext.wtf.html5 import EmailField
from wtforms.validators import Required


class TellYourStoryForm(Form):
    name = TextField('Name', validators=[Required()])
    email = EmailField('Email', validators=[Required()])
    story = TextAreaField('Story', validators=[Required()])
