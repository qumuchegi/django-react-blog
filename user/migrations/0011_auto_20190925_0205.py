# Generated by Django 2.2.5 on 2019-09-25 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20190925_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.ImageField(upload_to='user/static/user-upload/user-avatars/', verbose_name='头像'),
        ),
    ]
