from django.contrib import admin
from django.urls import path,include
from . import views

app_name='star'
urlpatterns = [
    path('givestar',views.giveStar),
]
