# Generated by Django 2.2.5 on 2019-09-30 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('star', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='star',
            name='star_for_comment_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='zan_to_blog', to='comment.Comment', verbose_name='赞的被给予方的评论的ID'),
        ),
    ]
