from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import Signal

from main.utilities import send_activation_notification, get_timestamp_path

class ShaUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Activated at")
    send_message = models.BooleanField(default=True, db_index=True, verbose_name="Send messages?")

    average_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True, verbose_name="Average rating")
    favorite = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers", verbose_name="Favorites")

    def delete(self, *args, **kwargs):
        for offer in self.offer_set.all():
            offer.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


user_registrated = Signal('instance')


def user_registrated_dispather(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispather)


class ShaUserAvatar(models.Model):
    user = models.OneToOneField(ShaUser, on_delete=models.CASCADE, related_name="avatar", verbose_name="User",)
    image = models.ImageField(verbose_name="Image")

    def __str__(self):
        return f'{self.user.username} photo - {self.image.url}'

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"


class Location(models.Model):
    user = models.OneToOneField(ShaUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User", related_name="location")
    offer = models.OneToOneField('main.Offer', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Offer', related_name="location")
    search_id = models.CharField(max_length=256, verbose_name="Search ID")
    name = models.CharField(max_length=256, verbose_name="Name")

    def __str__(self) -> str:
        return f"{self.name}"