from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from django.db.models import Avg

from .utilities import send_activation_notification, get_timestamp_path, send_comment_notification
from .utilities import send_chat_message_notification, send_review_notification


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True, verbose_name="Name")
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name="Order")
    super_category = models.ForeignKey('SuperCategory', on_delete=models.PROTECT, null=True, blank=True,
                                        verbose_name="Super category")
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name="Image")

    def __str__(self):
        super = self.super_category if self.super_category else "Super"
        return f"{super} - {self.name}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


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
        verbose_name = "Super category"
        verbose_name_plural = "Super categories"


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
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"


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


class UserReview(models.Model):
    RATING = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    author = models.ForeignKey(ShaUser, on_delete=models.DO_NOTHING, related_name="review", verbose_name="Author")
    offer = models.ForeignKey("Offer", on_delete=models.DO_NOTHING, related_name="review", verbose_name="Offer")
    reviewal = models.ForeignKey(ShaUser, on_delete=models.CASCADE, related_name="rating", verbose_name="Reviewal")
    speed = models.SmallIntegerField(default=5, choices=RATING,verbose_name="Speed")
    cost = models.SmallIntegerField(default=5, choices=RATING, verbose_name="Cost")
    accuracy = models.SmallIntegerField(default=5, choices=RATING, verbose_name="Accuracy")
    content = models.TextField(verbose_name="Review")
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created")

    def __str__(self):
        return f'Review of {self.author} for {self.reviewal} {self.offer} offer'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


def review_save_dispatcher(sender, **kwargs):
    reviewal = kwargs["instance"].reviewal
    user = reviewal.rating.aggregate(rating=(Avg('speed') + Avg('cost') + Avg('accuracy')) / 3)
    reviewal.average_rating = round(user['rating'], 1)
    reviewal.save()
    if kwargs["created"] and reviewal.send_message:
        send_review_notification(kwargs["instance"])


post_save.connect(review_save_dispatcher, sender=UserReview)


class Offer(models.Model):
    STATUS = [
        ('n', 'New'),
        ('a', 'Accepted'),
        ('d', 'Done')
    ]

    category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name="Category")
    title = models.CharField(max_length=64, verbose_name="Offer")
    content = models.TextField(verbose_name="Content")
    price = models.FloatField(default=0, verbose_name="Price")
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name="Image")
    author = models.ForeignKey(ShaUser, on_delete=models.CASCADE, verbose_name="Author")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Is active")
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created" )
    reviews = models.IntegerField(default=0, verbose_name="Reviews count")
    shared = models.IntegerField(default=0, verbose_name="Share count")
    status = models.CharField(max_length=1, default='n', null=True, blank=True, db_index=True, choices=STATUS, verbose_name="Status")
    winner = models.ForeignKey(ShaUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="accepted_offers" , verbose_name="Executant")

    def delete(self, *args, **kwargs):
        for image in self.additionalimage_set.all():
            image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/%i/%i/" % (self.category.id, self.id)

    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
        ordering = ["-created"]


class AdditionalImage(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, verbose_name="Offer")
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name="Image")

    class Meta:
        verbose_name = "Additional photo"
        verbose_name_plural = "Additional photos"


class Comment(models.Model):
    MEASUREMENTS = [
                ('h', 'Hour'),
                ('d', 'Day'),
                ('w', 'Week'),
                ('m', 'Month')
               ]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, verbose_name="Offer")
    author = models.ForeignKey(ShaUser, on_delete=models.CASCADE, verbose_name="Author")
    content = models.TextField(verbose_name="Content")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Is active")
    price = models.FloatField(default=0, null=True, blank=True, verbose_name="Price")
    time_amount = models.SmallIntegerField(default=0, null=True, blank=True, verbose_name="Time amount")
    measure = models.CharField(max_length=1, null=True, blank=True, choices=MEASUREMENTS, verbose_name="Measure")
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created")

    class Meta:
        ordering = ['created']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


def comment_save_dispatcher(sender, **kwargs):
    author = kwargs['instance'].offer.author
    if kwargs['created'] and author.send_message:
        send_comment_notification(kwargs['instance'])


post_save.connect(comment_save_dispatcher, sender=Comment)


class ChatMessage(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="chat_messages", verbose_name="Offer")
    author = models.ForeignKey(ShaUser, on_delete=models.CASCADE, related_name="sent_messages", verbose_name="Author")
    receiver = models.ForeignKey(ShaUser, on_delete=models.CASCADE, related_name="received_messages", verbose_name="Receiver")
    content = models.TextField(verbose_name="Message")
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created")

    class Meta:
        ordering = ["-created"]
        verbose_name = "Chat message"
        verbose_name_plural = "Chat messages"


def chat_save_dispatcher(sender, **kwargs):
    receiver = kwargs['instance'].receiver
    if kwargs['created'] and receiver.send_message:
        send_chat_message_notification(kwargs['instance'])


post_save.connect(chat_save_dispatcher, sender=ChatMessage)


class Location(models.Model):
    user = models.OneToOneField(ShaUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="User", related_name="location")
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Offer', related_name="location")
    search_id = models.CharField(max_length=256, verbose_name="Search ID")
    name = models.CharField(max_length=256, verbose_name="Name")

    def __str__(self) -> str:
        return f"{self.name}"
