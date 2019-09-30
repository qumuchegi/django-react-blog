# Generated by Django 2.2.5 on 2019-09-30 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0007_remove_comment_star_id'),
        ('message', '0005_auto_20190929_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='if_to_comment_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='comment.Comment', verbose_name='如果是对某一条评论的回复则该评论的ID'),
        ),
    ]
