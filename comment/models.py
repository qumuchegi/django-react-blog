from django.db import models

# Create your models here.

class Comment(models.Model):
  comment_id = models.AutoField(verbose_name='评论ID', primary_key=True)
  comment_blog_id = models.ForeignKey('blog.Blog',verbose_name="所属博客ID",on_delete=models.CASCADE,null=True)
  comment_owner_id = models.ForeignKey('user.User',verbose_name="评论主ID",on_delete=models.CASCADE,null=True)
  comment_content = models.TextField(verbose_name='评论内容', default='')
  created_time = models.DateTimeField(verbose_name='评论创建时间')

  def __str__(self):
      return self.comment_content