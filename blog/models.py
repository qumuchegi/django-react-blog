from django.db import models
# Create your models here.

class Blog(models.Model):
  blog_id = models.AutoField(verbose_name='博客ID', primary_key=True)
  author_id = models.ForeignKey('user.User',verbose_name="博主ID",null=True,on_delete=models.CASCADE)
  blog_title = models.CharField(verbose_name='博客标题', max_length=50,default='')
  blog_content = models.TextField(verbose_name='博客内容', default='')
  created_time = models.DateTimeField(verbose_name='博客创建时间')
  last_modified = models.DateTimeField(verbose_name='博客最后修改时间')
  is_publish = models.BooleanField(verbose_name='是否已经发布还是暂存(默认发布)',default=True)

  def __str__(self):
    return f'{self.blog_title}{self.blog_id}'


