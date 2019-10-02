from django.urls import path,include
from . import views

app_name='blog'
urlpatterns = [
    path('allmyblogs/',views.allmyblogs),
    path('createblog',views.createblog,name='createblog'),
    path('createblog/<int:blogid>',views.createblog,name='modifyblog'),
    path('blogdetails',views.getblog,name="blogdetails"),
    path('blogcomments/',views.getBlogComment),
    path('uploadimg',views.postimg),
    path('alltags/',views.getBlogAllTags)
]