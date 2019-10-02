from django.urls import path,include
from . import views

app_name='comment'
urlpatterns = [
    path('', views.postComment),
    path('mycomments',views.getMyComments)
]