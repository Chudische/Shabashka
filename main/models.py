from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal

from .utilities import send_activation_notification

# Create your models here.

class ShaUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Активирован")
    send_message = models.BooleanField(default=True, db_index=True, verbose_name="Отправлять оповещения?")
    
    class Meta(AbstractUser.Meta):
        pass

user_registred = Signal(providing_args=['instance'])

def user_registred_dispather(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

user_registred.connect(user_registred_dispather)