# Generated by Django 2.0.13 on 2019-04-18 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_auto_20190417_2133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='author',
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
    ]