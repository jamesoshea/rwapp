# Generated by Django 2.0.12 on 2019-07-25 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rw', '0002_supportingmember_date_signup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportingmember',
            name='surname',
        ),
    ]