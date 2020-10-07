from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal

from .utilities import send_activation_notification

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=20, unique=True, db_index=True, verbose_name="Название")
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name="Порядок")
    super_category = models.ForeignKey('SuperCategory', on_delete=models.PROTECT, null=True, blank=True,
                                        verbose_name="Надкатегория")

class SuperCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=True)


class SuperCategory(Category):
    objects = SuperCategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = "Надкатегория"
        verbose_name_plural = "Надкатегории"


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=False)

class SubCategory(Category):
    objects = SubCategoryManager()

    def __str__(self):
        return f"{self.super_category.name} - {self.name}"

    class Meta:
        proxy = True
        ordering = ('super_category__order', 'super_category__name', 'order', 'name')
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"




class ShaUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Активирован")
    send_message = models.BooleanField(default=True, db_index=True, verbose_name="Отправлять оповещения?")
    
    class Meta(AbstractUser.Meta):
        pass

user_registrated = Signal(providing_args=['instance'])

def user_registrated_dispather(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

user_registrated.connect(user_registrated_dispather)