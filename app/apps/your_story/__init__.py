from flask import Blueprint, flash, render_template, redirect, url_for
from google.appengine.api import mail

from .forms import TellYourStoryForm


recipients = 'andy.driver@thebbgroup.org'
#recipients = 'pressoffice@beatbullying.org, carina@thebbgroup.org'

your_story_app = Blueprint('your_story', __name__, template_folder='templates')

@your_story_app.route('/', methods=['GET', 'POST'])
def tell_me_it():
    form = TellYourStoryForm()

    if form.validate_on_submit():
        if not send_mail_to_press_office(**form.data):
            flash('Sorry! A problem occurred while sending your story, please '
                    'try again later.')
            return redirect(url_for('your_story.tell_me_it'))
        return redirect(url_for('your_story.kthxbai'))

    return render_template('your-story.jinja', form=form)

@your_story_app.route('/thanks')
def kthxbai():
    return render_template('your-story-kthxbai.jinja')

def send_mail_to_press_office(**data):
    try:
        msg = mail.EmailMessage(
                to=recipients,
                sender=data['email'],
                subject= "Ayden's Law: Tell Your Story",
                body=data['story'])
        msg.check_initialized()
        msg.send()
    except:
        return False
    return True
