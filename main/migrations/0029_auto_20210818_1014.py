# Generated by Django 3.1.6 on 2021-08-18 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20210726_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='search_id',
            field=models.BigIntegerField(verbose_name='ID для поиска'),
        ),
    ]
