# Generated by Django 2.2.5 on 2019-09-30 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blog_star_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='star_id',
        ),
    ]
