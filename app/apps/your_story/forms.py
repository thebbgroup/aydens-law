from flask.ext.wtf import Form, TextField
from wtforms.validators import Required


class TellYourStoryForm(Form):
    name = TextField('Name', validators=[Required()])
    email = TextField('Email', validators=[Required()])
    story = TextField('Story', validators=[Required()])
