# Generated by Django 3.1.3 on 2020-11-06 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20201106_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='price',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Предложить цену'),
        ),
    ]
