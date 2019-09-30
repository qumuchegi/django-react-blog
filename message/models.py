from django.db import models
from django.utils.timezone import now
# Create your models here.

class Message(models.Model):
  message_id = models.AutoField(verbose_name='消息ID', primary_key=True)
  content = models.TextField(verbose_name='消息内容', default='')
  sender_id = models.ForeignKey('user.User',verbose_name='发送者ID',on_delete=models.CASCADE,null=True,related_name='sender')
  receiver_id = models.ForeignKey('user.User',verbose_name='发送者ID',on_delete=models.CASCADE,null=True,related_name='receiver')
  send_time = models.DateField(verbose_name='发送时间',default=now)
  hadread = models.BooleanField(verbose_name='是否已读',default=False)
  msg_source_blog = models.ForeignKey('blog.Blog',verbose_name='消息来源博客ID',on_delete=models.CASCADE,null=True)
  if_to_comment_id = models.ForeignKey('comment.Comment',verbose_name='如果是对某一条评论的回复则该评论的ID',on_delete=models.CASCADE,null=True) 

  def __str__(self):
      return self.content[0:20] if len(self.content)>20 else self.content
  
