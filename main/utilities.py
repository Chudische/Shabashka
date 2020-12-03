from datetime import datetime
from os.path import splitext
from django.template.loader import render_to_string
from django.core.signing import Signer


from shabashka.settings import ALLOWED_HOSTS

signer = Signer()

def send_activation_notification(user):
    """ Send message to user with activation notification """
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'

    context = {'user': user, 'host': host,
                'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string("email/activation_letter_body.txt", context)
    user.email_user(subject, body_text)
    


def send_comment_notification(comment):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    author = comment.offer.author
    context = {'author': author, 'host': host, 'comment': comment}
    subject = render_to_string('email/new_comment_subject.txt', context)
    body_text = render_to_string('email/new_comment_body.txt', context)
    author.email_user(subject, body_text)
   


def send_chat_message_notification(message):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    receiver = message.receiver
    context = {'receiver': receiver, 'host': host, "offer": message.offer}
    subject = render_to_string('email/new_chat_message_subject.txt', context)
    body_text = render_to_string('email/new_chat_message_body.txt', context)
    reciever.email_user(subject, body_text)
    


def send_review_notification(message):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    receiver = message.reviewal
    context = {'receiver': receiver, 'host': host, "review": message}
    subject = render_to_string('email/new_review_subject.txt', context)
    body_text = render_to_string('email/new_review_body.txt', context)
    reciever.email_user(subject, body_text)
    


def get_timestamp_path(instanse, filename):
    """
    Create filename with timestamp
    """
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])
