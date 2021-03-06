# Generated by Django 3.1.3 on 2020-11-25 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20201124_1514'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shauseravatar',
            options={'verbose_name': 'Аватар', 'verbose_name_plural': 'Аватары'},
        ),
        migrations.CreateModel(
            name='UserReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speed', models.SmallIntegerField(default=5, verbose_name='Скорость')),
                ('cost', models.SmallIntegerField(default=5, verbose_name='Стоимость')),
                ('accuracy', models.SmallIntegerField(default=5, verbose_name='Качество')),
                ('content', models.TextField(verbose_name='Отзыв')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликован')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('reviewal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='raiting', to=settings.AUTH_USER_MODEL, verbose_name='Респондент')),
            ],
        ),
    ]
