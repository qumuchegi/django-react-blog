# Generated by Django 2.2.5 on 2019-09-25 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_remove_user_study_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.ImageField(upload_to='user-avatars/', verbose_name='头像'),
        ),
    ]
