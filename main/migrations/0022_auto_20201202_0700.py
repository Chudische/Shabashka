# Generated by Django 3.1.4 on 2020-12-02 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20201201_0825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationsettelment',
            name='district',
        ),
        migrations.RemoveField(
            model_name='locationsettelment',
            name='region',
        ),
        migrations.AlterField(
            model_name='shauser',
            name='location',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Населенный пункт'),
        ),
        migrations.DeleteModel(
            name='LocationDistrict',
        ),
        migrations.DeleteModel(
            name='LocationRegion',
        ),
        migrations.DeleteModel(
            name='LocationSettelment',
        ),
    ]
