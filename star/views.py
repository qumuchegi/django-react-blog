from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import json
from django.core.serializers import serialize
from .models import Star
from user.models import User
from blog.models import Blog
from comment.models import Comment
from user.middlewere import JWT_auth
# Create your views here.

@csrf_exempt
def giveStar(request):
  reqBody = json.loads(request.body.decode('utf8'))
  star_from_userid = reqBody['star_from_userid']
  star_to_userid = reqBody['star_to_userid']
  star_for_type = reqBody['star_for_type']
  star_for_id = reqBody['star_for_id']
  print('star_to_userid:', star_to_userid)
  if star_for_type=='blog':
    star_for_blog_id = star_for_id
    hadStared = Star.objects.get(star_from_userid=star_from_userid, star_for_blog_id=star_for_blog_id)
    if hadStared:
      return JsonResponse({'code':1}) # 已经赞过了
    new_star = Star(
      star_from_userid=User.objects.get(user_id=star_from_userid),
      star_to_userid=User.objects.get(user_id=star_to_userid),
      star_for_blog_id=Blog.objects.get(blog_id=star_for_blog_id)
    )
  else:
    '''
    先查询是否已经点过赞
    '''
    star_for_comment_id = star_for_id
    try:
       hadStared = Star.objects.get(star_from_userid=star_from_userid, star_for_comment_id=star_for_comment_id)
    except Star.DoesNotExist:
      new_star = Star(
        star_from_userid=User.objects.get(user_id=star_from_userid),
        star_to_userid=User.objects.get(user_id=star_to_userid),
        star_for_comment_id=Comment.objects.get(comment_id=star_for_comment_id)
      )
      new_star.save()
      return JsonResponse({'code': 0})
    else:
      if hadStared:
        return JsonResponse({'code':1}) # 已经赞过了
 
def getMyStarToOthers(request, star_direction):
  if not JWT_auth(request):
    return render(request,'notauthorized.html')
  userid = request.GET['userid']
  stars=[]

  if star_direction=='to-others':
    stars = Star.objects.filter(star_from_userid=userid)
    stars_from_user = User.objects.get(user_id=userid)
    stars_from_user = {
      'avatar': stars_from_user.avatar_url.url.replace('user/static/',''),
    }
  elif star_direction=='to-me':
    stars = Star.objects.filter(star_to_userid=userid)
    stars_to_user = User.objects.get(user_id=userid)
    stars_to_user = {
      'avatar': stars_to_user.avatar_url.url.replace('user/static/',''),
    }
  print("stars:", stars)
  stars_rewrite = []

  if star_direction=='to-others':
    for star in stars:
      #star_form_user = star.star_from_userid
      if star.star_for_blog_id:
        star_for_blog_id = star.star_for_blog_id.blog_id 
        star_for_blog_author = star.star_for_blog_id.author_id #User 类
        star_for_blog_title = star.star_for_blog_id.blog_title
        stars_rewrite.append({
          'star_type': 'blog',
          'star_for_blog_url': '127:0.0.0.0:8000/blog/blogdetails?blogid='+ str(star_for_blog_id)+'&userid='+str(star_for_blog_author.user_id),
          'star_for_blog_title': star_for_blog_title,
          'star_give_time': star.created_time,
          'star_for_blog_author_avatar': star_for_blog_author.avatar_url.url.replace('user/static/',''),
          'star_for_blog_author_name': star_for_blog_author.username,
        })
      elif star.star_for_comment_id:
        #star_for_comment_id = star.star_for_comment_id.comment_id
        star_for_comment_blog_id = star.star_for_comment_id.comment_blog_id.blog_id
        star_for_comment_blog_author_id = star.star_for_comment_id.comment_blog_id.author_id.user_id
        star_for_comment_blog_title = star.star_for_comment_id.comment_blog_id.blog_title
        star_for_comment_owner = star.star_for_comment_id.comment_owner_id
        stars_rewrite.append({
          'star_type': 'comment',
          'star_for_blog_url': '127:0.0.0.0:8000/blog/blogdetails?blogid='+str(star_for_comment_blog_id)+'&userid='+str(star_for_comment_blog_author_id),
          'star_for_blog_title': star_for_comment_blog_title,
          'star_give_time': star.created_time,
          'star_for_comment_owner_avatar': star_for_comment_owner.avatar_url.url.replace('user/static/',''),
          'star_for_comment_owner_name': star_for_comment_owner.username
        })
    print('stars_rewrite:', stars_rewrite)
    print('stars_from_user:', stars_from_user)
    return render(request, 'mystarout.html',{'stars': stars_rewrite,'stars_from_user': stars_from_user})

  elif star_direction=='to-me':
    for star in stars:
          #star_form_user = star.star_from_userid
          star_from_user = star.star_from_userid #User 类
          if star.star_for_blog_id:
            star_for_blog_title = star.star_for_blog_id.blog_title
            star_for_blog_id = star.star_for_blog_id.blog_id 
           
            stars_rewrite.append({
              'star_type': 'blog',
              'star_for_blog_url': '127:0.0.0.0:8000/blog/blogdetails?blogid='+ str(star_for_blog_id)+'&userid='+str(star_for_blog_author.user_id),
              'star_for_blog_title': star_for_blog_title,
              'star_give_time': star.created_time,
              'star_from_user_avatar': star_from_user.avatar_url.url.replace('user/static/',''),
              'star_from_user_name': star_from_user.username
            })
          elif star.star_for_comment_id:
            #star_for_comment_id = star.star_for_comment_id.comment_id
            star_for_comment_blog_id = star.star_for_comment_id.comment_blog_id.blog_id
            star_for_comment_blog_author_id = star.star_for_comment_id.comment_blog_id.author_id.user_id
            star_for_comment_blog_title = star.star_for_comment_id.comment_blog_id.blog_title
            star_for_comment_owner = star.star_for_comment_id.comment_owner_id
            stars_rewrite.append({
              'star_type': 'comment',
              'star_for_blog_url': '127:0.0.0.0:8000/blog/blogdetails?blogid='+str(star_for_comment_blog_id)+'&userid='+str(star_for_comment_blog_author_id),
              'star_for_blog_title': star_for_comment_blog_title,
              'star_give_time': star.created_time,
              'star_from_user_avatar': star_from_user.avatar_url.url.replace('user/static/',''),
              'star_from_user_name': star_from_user.username
            })
    print('stars_rewrite:', stars_rewrite)
    print('stars_from_user:', stars_to_user)
    return render(request, 'starstome.html',{'stars': stars_rewrite,'stars_to_user': stars_to_user})



