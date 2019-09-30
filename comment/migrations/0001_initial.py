# Generated by Django 2.2.5 on 2019-09-27 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False, verbose_name='评论ID')),
                ('comment_owner_id', models.IntegerField(verbose_name='评论主ID')),
                ('comment_content', models.TextField(default='', verbose_name='评论内容')),
                ('created_time', models.DateTimeField(verbose_name='评论创建时间')),
            ],
        ),
    ]
