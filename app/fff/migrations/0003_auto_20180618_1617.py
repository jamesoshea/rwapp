# Generated by Django 2.0.5 on 2018-06-18 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fff', '0002_auto_20180616_0127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bikedonation',
            name='message',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='bikedonation',
            name='status',
            field=models.TextField(null=True),
        ),
    ]