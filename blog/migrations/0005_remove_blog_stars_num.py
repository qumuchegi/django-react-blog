# Generated by Django 2.2.5 on 2019-09-30 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190928_1108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='stars_num',
        ),
    ]