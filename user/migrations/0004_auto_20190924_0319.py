# Generated by Django 2.2.5 on 2019-09-24 03:19

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_avatar_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='/upload-files/user-avatars/avatar_default.png'), upload_to='', verbose_name='头像'),
        ),
    ]
