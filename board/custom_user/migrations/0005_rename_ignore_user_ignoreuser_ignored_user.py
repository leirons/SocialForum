# Generated by Django 3.2.5 on 2021-07-26 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0004_customuser_subscribers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ignoreuser',
            old_name='ignore_user',
            new_name='ignored_user',
        ),
    ]
