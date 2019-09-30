from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import json
from django.core.serializers import serialize
from .models import Message
from user.models import User
from blog.models import Blog
from comment.models import Comment
# Create your views here.

@csrf_exempt
def postMessage(request, msg_from_comment={}):
  if msg_from_comment:
    sender_id = msg_from_comment['sender_id']
    receiver_id = msg_from_comment['receiver_id']
    content = msg_from_comment['content']
    blogid = msg_from_comment['blogid']
  else:
    reqBody = json.loads(request.body.decode('utf8'))
    sender_id = reqBody['sender_id']
    receiver_id = reqBody['receiver_id']
    content = reqBody['content']
    blogid = reqBody['blogid']
    comment_id = reqBody['commentid']

  m = Message(
    content=content
  )
  
  m.sender_id = User.objects.get(user_id=sender_id)
  m.receiver_id = User.objects.get(user_id=receiver_id)
  m.msg_source_blog = Blog.objects.get(blog_id=blogid)
  if not msg_from_comment:
    m.if_to_comment_id = Comment.objects.get(comment_id=comment_id)
  m.save()

  
  return JsonResponse({'code':0})

def getNotReadMsg(request):
  userid = request.GET['userid']
  not_read_msgs_with_senderInfo = []

  not_read_msgs = Message.objects.filter(receiver_id=userid,hadread=False)
  #print('json序列化前的未读消息：',json.loads(serialize('json',not_read_msgs))[0]['fields']['sender_id'])
  json_msgs = serialize('json',not_read_msgs)
  json_msgs = json.loads(json_msgs)
  print('未读消息：',json_msgs)
  '''
   在外键里面填充发送者信息
  '''
  for msg in not_read_msgs: 
    not_read_msgs_with_senderInfo.append({
      'msg_id':msg.pk,
      'sender_avatar': str(msg.sender_id.avatar_url),
      'sender_name': msg.sender_id.username,
      'sender_id': msg.sender_id.user_id,
      'msg_content': msg.content,
      'send_time': msg.send_time,
      'source_blog': json.loads(serialize('json', [msg.msg_source_blog]))[0]
    })

  return JsonResponse({'code':0, 'msgs':not_read_msgs_with_senderInfo})

@csrf_exempt
def readMsg(request):
  reqBody = json.loads(request.body.decode('utf8'))
  msgid = reqBody['msg_id']

  m = Message.objects.get(message_id=msgid)
  m.hadread = True
  m.save()
  
  return JsonResponse({'code':0})

@csrf_exempt
def readManyMsgs(request):
  reqBody = json.loads(request.body.decode('utf8'))
  msg_ids = reqBody['msg_ids']

  print('要读的消息ID：',msg_ids)
  for msgid in msg_ids:
    m = Message.objects.get(message_id=msgid)
    m.hadread = True
    m.save()
  
  return JsonResponse({'code':0})

