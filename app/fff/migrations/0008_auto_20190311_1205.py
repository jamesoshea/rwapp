# Generated by Django 2.0.6 on 2019-03-11 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fff', '0007_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]