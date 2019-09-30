from django.shortcuts import render
from blog.middlewere import allpubblogs
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import json
from django.core.serializers import serialize

def get_home_page(request):
  return render(request, 'home.html')

def get_all_pub_blogs(request):
  pageNum=int(request.GET['pageNum'])
  pageSize=5
  blogs_per_page = allpubblogs(pageNum,pageSize)
  #print(f'首页第{pageNum}页加载博客:',blogs_per_page)
  #blogs_json = json.loads(serialize('json',blogs_per_page))
  return JsonResponse({'code':0, 'blogs':blogs_per_page})