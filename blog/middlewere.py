import json
from django.core.serializers import serialize
from .models import Blog
from user.models import User
from message.models import Message
from django.core.paginator import Paginator #分页

def allpubblogs(pageNum,pageSize):
  blogs = []
  print(int((pageNum-1)*pageSize),int(pageNum*pageSize))
  try:
    for blog in Blog.objects.filter(is_publish=True)[int((pageNum-1)*pageSize):int(pageNum*pageSize)]:
      blogs.append(add_authorInfo_to_blog(blog))
  except Blog.DoesNotExist:
    pass
  #paginator = Paginator(blogs,10) # 每页10条
  return blogs


def add_authorInfo_to_blog(blog):
  print('author avatar:', blog.author_id.avatar_url.url.replace('user/static/',''))
  return {
    'blog_id': blog.blog_id,
    'author_name': blog.author_id.username,
    'author_id': blog.author_id.user_id,
    'author_avatar': blog.author_id.avatar_url.url.replace('user/static/',''),
    'blog_last_modified': blog.last_modified,
    'blog_content': blog.blog_content,
    'blog_title': blog.blog_title
  }

def getBlogCommentReply(commentid):
  '''
  获取某个博客的每一条评论下的回复
  '''
  try:
    msgs = Message.objects.filter(if_to_comment_id=commentid)
    msgs_json = []
    for msg in msgs:
      from_user =  json.loads(serialize('json',[msg.sender_id]))[0]

      msgs_json.append({
          'reply_to_comment_id': commentid,
          'reply_content': msg.content,
          'reply_from_user_id': msg.sender_id.pk,
          'reply_from_user_avatar': from_user['fields']['avatar_url'],
          'reply_from_user_name': from_user['fields']['username'],
          'reply_time': msg.send_time
        })
    return msgs_json
  except Message.DoesNotExist:
    return []