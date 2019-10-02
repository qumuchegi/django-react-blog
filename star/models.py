from django.db import models
from django.utils.timezone import now
# Create your models here.

class Star(models.Model):
  '''
  赞是对博客、评论的赞
  '''
  star_id = models.AutoField(verbose_name='赞ID', primary_key=True)
  star_from_userid = models.ForeignKey('user.User',verbose_name='赞的发送者ID',on_delete=models.CASCADE,null=True,related_name='star_from')
  star_to_userid = models.ForeignKey('user.User',verbose_name='赞的接受者ID',on_delete=models.CASCADE,null=True,related_name='star_to')
  '''
  如果赞是给博客的：
  '''
  star_for_blog_id = models.ForeignKey('blog.Blog',verbose_name='赞的被给予方的博客的ID',on_delete=models.CASCADE,null=True,related_name='zan_to_blog')
  '''
  如果赞是给评论的：
  '''
  star_for_comment_id = models.ForeignKey('comment.Comment',verbose_name='赞的被给予方的评论的ID',on_delete=models.CASCADE,null=True,related_name='zan_to_blog')
  created_time = models.DateTimeField(verbose_name='赞的时间',default=now)

  def __str__(self):
    return self.star_from_userid.username