from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class ShaUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Активирован")
    send_message = models.BooleanField(default=True, db_index=True, verbose_name="Отправлять оповещения?")
    
    class Meta(AbstractUser.Meta):
        pass
