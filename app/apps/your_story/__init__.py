from flask import Blueprint, render_template, redirect, url_for
from flask.ext.mail import Message

from app import app, mail

from .forms import TellYourStoryForm


your_story_app = Blueprint('your_story', __name__, template_folder='templates')

@your_story_app.route('/', methods=['GET', 'POST'])
def tell_me_it():
    form = TellYourStoryForm()

    if form.validate_on_submit():
        send_mail_to_press_office(**form.data)
        return redirect(url_for('tell_your_story.thanks'))

    return render_template('your-story.jinja', form=form)

@your_story_app.route('/thanks')
def kthxbai():
    return render_template('your-story-kthxbai.jinja')

def send_mail_to_press_office(**data):
    data['subject'] = "Ayden's Law: Tell Your Story"
    msg = Message(
            data['subject'],
            sender=data.email,
            recipients=['pressoffice@beatbullying.org'])
    msg.body = ("From: %(name) <%(email)>\n"
            "Subject: %(subject)\n\n"
            "%(story)") % data
    mail.send(msg)
