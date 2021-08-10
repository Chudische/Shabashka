from django.db import models
from django.contrib.gis.db.models import PointField
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from django.db.models import Avg

from .utilities import send_activation_notification, get_timestamp_path, send_comment_notification
from .utilities import send_chat_message_notification, send_review_notification
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

    average_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True, verbose_name="Средний рейтинг")
    favorite = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers", verbose_name="Избранное")
    def delete(self, *args, **kwargs):
        for offer in self.offer_set.all():
            offer.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass

user_registrated = Signal(providing_args=['instance'])

def user_registrated_dispather(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

user_registrated.connect(user_registrated_dispather)


class ShaUserAvatar(models.Model):
    user = models.OneToOneField(ShaUser, on_delete=models.CASCADE, related_name="avatar", verbose_name="Пользователь",)
    image = models.ImageField(verbose_name="Аватар")

    def __str__(self):
        return f'{self.user.username} photo - {self.image.url}'

    class Meta:
        verbose_name = "Аватар"
        verbose_name_plural = "Аватары"


class UserReview(models.Model):
    RATING = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    author = models.ForeignKey(ShaUser, on_delete=models.DO_NOTHING, related_name="review", verbose_name="Автор")
    offer = models.ForeignKey("Offer", on_delete=models.DO_NOTHING, related_name="review", verbose_name="Предложение")
    reviewal = models.ForeignKey(ShaUser, on_delete=models.CASCADE, related_name="rating", verbose_name="Респондент")
    speed = models.SmallIntegerField(default=5, choices=RATING,verbose_name="Скорость")
    cost = models.SmallIntegerField(default=5, choices=RATING, verbose_name="Стоимость")
    accuracy = models.SmallIntegerField(default=5, choices=RATING, verbose_name="Качество")
    content = models.TextField(verbose_name="Отзыв")
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликован")

    def __str__(self):
        return f'Отзыв {self.author} на {self.reviewal} в предложении {self.offer}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

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
        ('n', 'Новое'),
        ('a', 'Принято'),
        ('d', 'Выполнено')
    ]

    category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name="Категория")
    title = models.CharField(max_length=64, verbose_name="Предложение")
    content = models.TextField(verbose_name="Описание")
    price = models.FloatField(default=0, verbose_name="Цена")
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name="Фото")
    author = models.ForeignKey(ShaUser, on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Активное")
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано" )
    reviews = models.IntegerField(default=0, verbose_name="Просмотров")
    shared = models.IntegerField(default=0, verbose_name="Поделились")
    status = models.CharField(max_length=1, default='n', null=True, blank=True, db_index=True, choices=STATUS, verbose_name="Статус")
    winner = models.ForeignKey(ShaUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="accepted_offers" , verbose_name="Исполнитель")

    def delete(self, *args, **kwargs):
        for image in self.additionalimage_set.all():
            image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "/%i/%i/" % (self.category.id,self.id)

    class Meta:
        verbose_name = "Предложение"
        verbose_name_plural = "Предложения"
        ordering = ["-created"]


class AdditionalImage(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, verbose_name="Предложение")
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name="Фото")

    class Meta:
        verbose_name = "Дополнительное фото"
        verbose_name_plural = "Дополнительные фото"


class Comment(models.Model):
    MEASUREMENTS = [
                ('h', 'Час'),
                ('d', 'День'),
                ('w', 'Неделя'),
                ('m', 'Месяц')
               ]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, verbose_name="Предложение")
    author = models.ForeignKey(ShaUser, on_delete=models.CASCADE, verbose_name="Автор")
    content = models.TextField(verbose_name="Коментарий")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Выводить на экран")
    price = models.FloatField(default=0, null=True, blank=True, verbose_name="Предложить цену")
    time_amount = models.SmallIntegerField(default=0, null=True, blank=True, verbose_name="Сделаю за")
    measure = models.CharField(max_length=1, null=True, blank=True, choices=MEASUREMENTS, verbose_name="Еденица времени")
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Написан")


    class Meta:
        ordering = ['created']
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"

def comment_save_dispatcher(sender, **kwargs):
    author = kwargs['instance'].offer.author
    if kwargs['created'] and author.send_message:
        send_comment_notification(kwargs['instance'])

post_save.connect(comment_save_dispatcher, sender=Comment)


class ChatMessage(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="chat_messages", verbose_name="Предложение")
    author = models.ForeignKey(ShaUser, on_delete=models.CASCADE, related_name="sent_messages", verbose_name="Автор")
    receiver = models.ForeignKey(ShaUser, on_delete=models.CASCADE, related_name="received_messages", verbose_name="Получатель")
    content = models.TextField(verbose_name="Сообщение")
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Создано")

    class Meta:
        ordering = ["-created"]
        verbose_name = "Чат-сообщение"
        verbose_name_plural = "Чат-сообщения"

def chat_save_dispatcher(sender, **kwargs):
    receiver = kwargs['instance'].receiver
    if kwargs['created'] and receiver.send_message:
        send_chat_message_notification(kwargs['instance'])


post_save.connect(chat_save_dispatcher, sender=ChatMessage)


class Location(models.Model):
    user = models.OneToOneField(ShaUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь", related_name="location")
    offer = models.OneToOneField(Offer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Предложение', related_name="location")
    search_id = models.IntegerField(verbose_name="ID для поиска")
    name = models.CharField(max_length=256, verbose_name="Назване")

    def __str__(self) -> str:
        return f"{self.name}"
