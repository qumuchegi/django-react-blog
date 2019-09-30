from django.urls import path,include
from . import views

app_name='user'
urlpatterns = [
    path('register/', views.register,name='register'),
    path('login/',views.login,name='login'),
    path('mypage/',views.mypage),
    path('userinfo/',views.getUser)
]