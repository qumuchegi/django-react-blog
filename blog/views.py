from django.shortcuts import render
from .models import Blog
from django.http import JsonResponse
import time
from django.views.decorators.csrf import csrf_exempt 
import json
from django.core.serializers import serialize
from user.models import User
from user.middlewere import JWT_auth
from .middlewere import getBlogCommentReply

# Create your views here.
def allmyblogs(request):
  myid = request.GET['userid']
  blogs=[]
  try:
    blogs = Blog.objects.filter(author_id=myid)
  except Blog.DoesNotExist:
    pass
  '''
  查询对象必须要序列化为 json
  '''
  json_data = serialize('json', blogs) # str
  json_data = json.loads(json_data) # 序列化成json对象
  return JsonResponse({'blogs': json_data})

@csrf_exempt #屏蔽 CSRF
def createblog(request,blogid=''):#只有修改已有博客的时候才会有参数 blogid
  if request.method == 'GET':
     if not blogid:
        return render(request, 'create-new-blog.html')
     elif blogid:
        blog = Blog.objects.get(blog_id=blogid)
        blog_title = blog.blog_title
        blog_content = blog.blog_content
        return render(request,'create-new-blog.html',{'blog_title':blog_title, 'blog_content':blog_content})
  elif request.method == 'POST':
    print('修改博客ID:',blogid)
    '''
    授权认证
    '''
    '''
    if not JWT_auth(request):
      return JsonResponse({'code':1, 'msg':'您未经授权，不能修改此博客'})
    '''
    reqData_str = request.body.decode('utf8')
    reqData_obj = json.loads(reqData_str)
    print('post date:', reqData_obj)
    userid = reqData_obj['userid']
    blogContent = reqData_obj['content']
    blogTitle = reqData_obj['title']

    try:
      is_publish = reqData_obj['isPublish']
    except:
      is_publish = True

    if not blogid:#创建新博客模式
      newBlog = Blog(
        author_id=User.objects.get(user_id=userid), 
        blog_title=blogTitle, 
        blog_content=blogContent,
        created_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) ,
        last_modified=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        is_publish=is_publish
        )
      newBlog.save()
      return JsonResponse({'msg':'博客创建成功，已经入库！', 'code': 0})

    elif blogid:# 修改模式
      blog = Blog.objects.get(blog_id=blogid)
      blog.blog_content = blogContent
      blog.blog_title = blogTitle
      blog.save()
      return JsonResponse({'msg':'博客修改成功，已经入库！', 'code': 0})

    

@csrf_exempt #屏蔽 CSRF
def getblog(request):
  if request.method == 'GET':
    return render(request,'blog-details.html')
  elif request.method == 'POST':
    reqBody = json.loads(request.body.decode('utf8'))
    blogid = reqBody['blogid']
    authorid = reqBody['authorid']
    print('blogid:',blogid)
    blog = [Blog.objects.get(blog_id=blogid)]
    user = [User.objects.get(user_id=authorid)]
    '''
    查询对象必须要序列化为 json
    '''
    json_blog_data = serialize('json', blog) # str
    json_blog_data = json.loads(json_blog_data) # 序列化成json对象
    json_user_data = serialize('json', user) # str
    json_user_data = json.loads(json_user_data) # 序列化成json对象
    return JsonResponse({'blog':json_blog_data, 'author':json_user_data, 'code':0})

def getBlogComment(request):
  blogid = request.GET['blogid']
  blog = Blog.objects.get(blog_id=blogid)
    
  #comments = [ele for ele in blog.comment_set.all()]
  comments_width_ownerinfo = []
  
  json_comments_data = serialize('json', blog.comment_set.all()) # str
  json_comments_data = json.loads(json_comments_data) # 序列化成json对象

  for comment_ele in json_comments_data:
      #print('每一次循环：',comment_ele['fields'])
      userid = comment_ele['fields']['comment_owner_id']
      user = User.objects.get(user_id=userid)
      user = json.loads(serialize('json',[user]))[0]
      #print('user:', user)
      comment_reply = getBlogCommentReply(comment_ele['pk'])

      comments_width_ownerinfo.append({
        'comment_id': comment_ele['pk'],
        'comment_content': comment_ele['fields']['comment_content'],
        'owner_id': comment_ele['fields']['comment_owner_id'],
        'owner_name': user['fields']['username'],
        'created_time': comment_ele['fields']['created_time'],
        'avatar': user['fields']['avatar_url'],
        'comment_reply': comment_reply
        #'comment_owner_details_info': user
      })
  #print(blog,comments_width_ownerinfo)

  '''
  jsonData = serialize('json',comments_width_ownerinfo)
  jsonData = json.loads(jsonData)
  '''
  return JsonResponse({'comments':comments_width_ownerinfo ,'code':0})



