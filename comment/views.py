from django.shortcuts import render
from django.http import JsonResponse
import time
from django.views.decorators.csrf import csrf_exempt 
import json
from django.core.serializers import serialize
from .models import Comment
from blog.models import Blog
from user.models import User
from message.views import postMessage

# Create your views here.

@csrf_exempt #屏蔽 CSRF
def postComment(request):
  reqBody = json.loads(request.body.decode('utf8'))
  comment_owner_id = reqBody['readerid']
  comment_content = reqBody['commentContent']
  blogid = reqBody['blogid']
  c = Comment(
    comment_content=comment_content,
    created_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
  )
  b = Blog.objects.get(blog_id=blogid)
  c.comment_blog_id=b
  u = User.objects.get(user_id=comment_owner_id)
  c.comment_owner_id = u

  c.save()

  '''
  同时将评论送消息数据库
  '''
  postMessage(request,
    {
      'sender_id': comment_owner_id, 
      'receiver_id': b.author_id.user_id, 
      'content': comment_content,
      'blogid': blogid,
    })
  
  return JsonResponse({'code':0})

def getMyComments(request):
  userid = request.GET['userid']
  comments = Comment.objects.filter(comment_owner_id=userid)
  comments_rewrite = []
  user = User.objects.get(user_id=userid)
  user = {
    'avatar': user.avatar_url.url.replace('user/static/','')
  }
  for comment in comments:
    comment_blog_id = comment.comment_blog_id.blog_id
    comment_blog_title = comment.comment_blog_id.blog_title
    comment_blog_author_id =  comment.comment_blog_id.author_id.user_id
    comment_time = comment.created_time
    comment_content = comment.comment_content
    comments_rewrite.append({
      'comment_blog_title': comment_blog_title,
      'comment_time': comment_time,
      'comment_content': comment_content,
      'comment_blog_url': '127:0.0.0.0:8000/blog/blogdetails?blogid='+ str(comment_blog_id)+'&userid='+str(comment_blog_author_id),
    })
  return render(request, 'mycomments.html',{'comments': comments_rewrite, 'user': user})