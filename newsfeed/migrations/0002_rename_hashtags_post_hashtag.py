# Generated by Django 4.1.5 on 2023-05-27 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsfeed', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='hashtags',
            new_name='hashtag',
        ),
    ]
