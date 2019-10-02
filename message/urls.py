from django.contrib import admin
from django.urls import path,include
from . import views

app_name='message'
urlpatterns=[
  path('',views.postMessage),
  path('readmsg/',views.readMsg),
  path('readmanymsgs',views.readManyMsgs),
  path('msgnotread/',views.getNotReadMsg),
  path('historymsgs/',views.getMyHistoryMsgs)
]