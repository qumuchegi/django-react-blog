# Generated by Django 2.2.5 on 2019-09-30 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0006_comment_star_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='star_id',
        ),
    ]
