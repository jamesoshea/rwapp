# Generated by Django 2.0.6 on 2019-03-11 12:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fff', '0008_auto_20190311_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='date',
            field=models.DateField(default=datetime.datetime.now, help_text='The date that will be shown on the website as the date of this news entry'),
        ),
        migrations.AddField(
            model_name='news',
            name='headline',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='news',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
