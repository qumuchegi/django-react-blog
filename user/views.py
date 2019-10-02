#coding=utf-8
import random
import string
import time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.urls import reverse
from .middlewere import generate_JWT_token,JWT_auth,decode_JWT_token
from .forms.register import Register
from .forms.login import Login
from .models import User
algrithms = 'pbkdf2_sha256' #对用户密码加密使用的算法
from django.views.decorators.csrf import csrf_exempt 

def register(request):
  """
  用户注册，使用表单系统
  """
  program_lans = ['javascript','Python','C++','C','Node']
  if request.method == 'GET':
    register_form = Register()
    return render(request, 'register.html',{'register_form': register_form, 'program_lans': program_lans})
  elif request.method == 'POST':
    register_form_res = Register( request.POST )
    if register_form_res.is_valid():
      user_name = request.POST['user_name']
      password = request.POST['password']
      password_again = request.POST['password_again']
      avatar = request.FILES['avatar']
      sex = request.POST['sex']
      #program_lan = request.POST['program_lan']
      program_lan = []
      for lan in program_lans:
        try:
          lan = request.POST[lan]
        except :
          continue
        program_lan.append(lan)
      print(user_name,password,password_again,avatar,sex,program_lan)
      try:
        had_same_username = User.objects.get(username=user_name)
        print(had_same_username)
      except User.DoesNotExist:
        pass
      else:
        return render(request,'err.html',{'err_type':'已经有相同用户名','err_msg':'请重新选择其他用户名'})
      '''
      给密码加密后再存入数据库
      '''
      if password == password_again:
        salt = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890',20)) # 生成随机的盐
        print('盐：'+salt)
        password_salted = make_password(password, salt, algrithms)
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        new_user = User(
          username=user_name,
          password_encrypted=password_salted,
          password_salt=salt,
          created_time=now,
          avatar_url=avatar,
          program_lan='/'.join(program_lan),
        )
        new_user.save()
        return HttpResponseRedirect('/user/login') # 一定要在前面加 /，才是相对URL的重定向
      else:
        return render(request,'err.html',{'err_type':'密码不一致','err_msg':'请重写输入密码'})

def login(request):
  """
  用户登录，使用表单系统
  """
  if request.method == 'GET':
    login_form = Login()
    return render(request,'login.html',{'login_form':login_form})
  elif request.method == 'POST':
    login_form_res = Login(request.POST)
    if login_form_res.is_valid():
      user_name = request.POST['user_name']
      password = request.POST['password']
      try:
        user = User.objects.get(username=user_name)
      except User.DoesNotExist:
        return render(request,'err.html',{'err_type':'用户名不存在','err_msg':'请重写输入用户名'})
      else:
       password_encrypted = user.password_encrypted
       if check_password(password,password_encrypted): # 验证密码
         '''
          响应头加入对已登录用户的授权 token
         '''
         payload = {
           'userid': user.user_id,
           'expire': int(time.time()+60*60*24),
           'username': user.username
         }
         #payload = json.loads(serialize('json', [payload]))
         jwt_token = generate_JWT_token(payload)
         print('jwt:',jwt_token)
         res = HttpResponseRedirect('/')
         res.set_cookie('jwt_token', jwt_token, max_age=60*60*24)
         res.set_cookie('logined_user_userid', user.user_id, max_age=60*60*24)
         return res
       else:
         return render(request,'err.html',{'err_type':'密码不正确','err_msg':'请重写输入密码'})

def mypage(request):
  if not JWT_auth(request):
    return render(request,'notauthorized.html')

  userid = request.GET['userid']

  try:
    user = User.objects.get(user_id=userid)
  except User.DoesNotExist:
    return render(request,'err.html',{'err_type':'用户名不存在','err_msg':'请重写输入用户名'})
  
  return render(request,'mypage.html',
    {
      'username':user.username, 
      'sex':user.sex,
      'userid': user.user_id,
      'avatar':user.avatar_url.url.replace('user/static/',''),
      'program_lan':user.program_lan.split('/'),
      #'myblog': user.blog
    })

def getUser(request):
  userid = request.GET['userid']
  user = []
  try:
    user = User.objects.get(user_id=userid)
  except User.DoesNotExist:
    pass
  #user_json = json.loads(serialize('json',[user]))
  user_rewrite = {
    'username': user.username,
    'sex': user.sex,
    'avatar_url': user.avatar_url.url,
    'program_lan': user.program_lan
  }
  return JsonResponse({'code':0,'user':user_rewrite})