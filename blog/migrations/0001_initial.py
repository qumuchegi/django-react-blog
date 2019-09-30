# Generated by Django 2.2.5 on 2019-09-27 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('blog_id', models.AutoField(primary_key=True, serialize=False, verbose_name='博客ID')),
                ('author_id', models.IntegerField(verbose_name='博主ID')),
                ('blog_title', models.CharField(default='', max_length=50, verbose_name='博客标题')),
                ('blog_content', models.TextField(default='', verbose_name='博客内容')),
                ('created_time', models.DateTimeField(verbose_name='博客创建时间')),
                ('last_modified', models.DateTimeField(verbose_name='博客最后修改时间')),
            ],
        ),
    ]
