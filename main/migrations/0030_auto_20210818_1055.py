# Generated by Django 3.1.6 on 2021-08-18 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20210818_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='search_id',
            field=models.CharField(max_length=256, verbose_name='ID для поиска'),
        ),
    ]
