# Generated by Django 2.2.5 on 2019-09-27 12:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0011_auto_20190925_0205'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False, verbose_name='消息ID')),
                ('content', models.TextField(default='', verbose_name='消息内容')),
                ('send_time', models.DateField(default=django.utils.timezone.now, verbose_name='发送时间')),
                ('receiver_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiverUser', to='user.User', verbose_name='发送者ID')),
                ('sender_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='senderUser', to='user.User', verbose_name='发送者ID')),
            ],
        ),
    ]