from django.db import models
from django.core.files.storage import FileSystemStorage
#fs = FileSystemStorage(location='/upload-files/user-avatars/')
# Create your models here.

class User(models.Model):
  user_id = models.AutoField(primary_key=True)
  username = models.CharField(verbose_name='用户名', max_length=10)
  password_encrypted = models.CharField(verbose_name='被加密后的密码', max_length=2000) # 
  password_salt = models.CharField(verbose_name='对密码加盐时使用的盐',max_length=100)
  avatar_url = models.ImageField(verbose_name='头像',upload_to='user/static/user-upload/user-avatars/')
  sex = models.CharField(verbose_name='性别',max_length=1,default='男')
  program_lan = models.CharField(verbose_name='语言', max_length=100,default='javascript')
  created_time = models.DateTimeField(verbose_name='创建时间')

  def __str__(self):
    return f'{self.username}{self.user_id}'

 
