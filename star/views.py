from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import json
from django.core.serializers import serialize
from .models import Star
from user.models import User
from blog.models import Blog
from comment.models import Comment
# Create your views here.

@csrf_exempt
def giveStar(request):
  reqBody = json.loads(request.body.decode('utf8'))
  star_from_userid = reqBody['star_from_userId']
  star_for_type = reqBody['star_for_type']
  star_for_id = reqBody['star_for_id']
  if star_for_type=='blog':
    star_for_blog_id = star_for_id
    new_star = Star(
      star_from_userid=User.objects.get(user_id=star_from_userid),
      star_for_blog_id=Blog.objects.get(blog_id=star_for_blog_id)
    )
  else:
    star_for_comment_id = star_for_id
    new_star = Star(
      star_from_userid=User.objects.get(user_id=star_from_userid),
      star_for_comment_id=Comment.objects.get(comment_id=star_for_comment_id)
    )
  new_star.save()
  return JsonResponse({'code': 0})
  