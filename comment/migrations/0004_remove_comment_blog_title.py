# Generated by Django 2.2.5 on 2019-09-27 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_auto_20190927_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='blog_title',
        ),
    ]