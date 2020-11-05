from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal

from .utilities import send_activation_notification, get_timestamp_path, send_comment_notification

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


class LocationRegion(models.Model):
    name = models.CharField(max_length=64, unique=True, db_index=True, verbose_name="Область")

    def __str__(self):
        return f"{self.name} область"

    class Meta:
        ordering = ['name']
        verbose_name = "Область"
        verbose_name_plural = "Области"


class LocationDistrict(models.Model):
    region = models.ForeignKey(LocationRegion, on_delete=models.PROTECT, verbose_name="В области")
    name = models.CharField(max_length=64, unique=True, db_index=True, verbose_name="Район")

    def __str__(self):
        return f"{self.region} область - {self.name} район"

    class Meta:
        ordering = ('region__name', 'name')
        verbose_name = "Район"
        verbose_name_plural = "Районы"


class LocationSettelment(models.Model):
    region = models.ForeignKey(LocationRegion, on_delete=models.PROTECT, verbose_name="В области")
    district = models.ForeignKey(LocationDistrict, on_delete=models.PROTECT, verbose_name="В районе")
    name = name = models.CharField(max_length=64, unique=True, db_index=True, verbose_name="Населенный пункт")

    def __str__(self):
        return f"{self.region} область- {self.district} район - {self.name}"

    class Meta:
        ordering = ('region__name', 'district__name', 'name')
        verbose_name = "Населенный пункт"
        verbose_name_plural = "Населенные пункты"


class ShaUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name="Активирован")
    send_message = models.BooleanField(default=True, db_index=True, verbose_name="Отправлять оповещения?")
    location = models.ForeignKey(LocationSettelment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Населенный пункт" )

    def delete(self, *args, **kwargs):
        for offer in self.offer_set.all():
            offer.delete()
        self.avatar.delete()
        super().delete(*args, **kwargs)


    class Meta(AbstractUser.Meta):
        pass


class ShaUserAvatar(models.Model):
    user = models.OneToOneField(ShaUser, on_delete=models.CASCADE, related_name="avatar", verbose_name="Пользователь",)
    avatar = models.ImageField(verbose_name="Аватар")


user_registrated = Signal(providing_args=['instance'])

def user_registrated_dispather(sender, **kwargs):
    send_activation_notification(kwargs['instance'])

user_registrated.connect(user_registrated_dispather)


class Offer(models.Model):
    STATUS = [
        ('n', 'Новое'),
        ('a', 'Принято'),
        ('d', 'Выполнено')
    ]

    category = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name="Категория")
    title = models.CharField(max_length=40, verbose_name="Предложение")
    content = models.TextField(verbose_name="Описание")
    price = models.FloatField(default=0, verbose_name="Цена")
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name="Фото")
    author = models.ForeignKey(ShaUser, on_delete=models.CASCADE, verbose_name="Автор")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Активное")
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано" )
    reviews = models.IntegerField(default=0, verbose_name="Просмотров")
    shared = models.IntegerField(default=0, verbose_name="Поделились")
    status = models.CharField(max_length=1, default='n', null=True, blank=True, db_index=True, choices=STATUS, verbose_name="Статус")
    
    def delete(self, *args, **kwargs):
        for image in self.additionalimage_set.all():
            image.delete()
        super().delete(*args, **kwargs)


    def __str__(self):
        return self.title

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
    price = models.FloatField(default=0, verbose_name="Предложить цену")
    time_amount = models.SmallIntegerField(default=0, verbose_name="Сделаю за")
    measure = models.CharField(max_length=1, null=True, blank=True, choices=MEASUREMENTS, verbose_name="Еденица времени")
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Написан")


    class Meta:
        ordering = ['created']
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"


def post_save_dispatcher(sender, **kwargs):
    author = kwargs['instance'].offer.author
    if kwargs['created'] and author.send_message:
        send_comment_notification(kwargs['instance'])

post_save.connect(post_save_dispatcher, sender=Comment)