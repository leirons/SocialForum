# Generated by Django 3.2.5 on 2021-07-22 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0002_alter_customuser_is_blocked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_blocked',
            field=models.BooleanField(default=False, verbose_name='Заблокировать пользователя'),
        ),
    ]
