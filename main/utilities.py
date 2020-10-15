from datetime import datetime
from os.path import splitext
from django.template.loader import render_to_string
from django.core.signing import Signer


from shabashka.settings import ALLOWED_HOSTS

signer = Signer()

def send_activation_notification(user):
    """ Send message to user with activation notification """
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS
    else:
        host = 'http://localhost:8000'

    context = {'user': user, 'host': host,
                'sign': signer.sign(user.username)}
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string("email/activation_letter_body.txt", context)
    print(subject, body_text)


def get_timestamp_path(instanse, filename):
    """
    Create filename with timestamp
    """
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])
    