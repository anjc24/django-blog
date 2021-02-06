from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

app_name = "posts"

urlpatterns = [
    path('', Index, name='Index'),
    path('detail/<int:pid>', detail, name='detail'),
    path('category/<int:cid>', category, name='category'),
    path('userposts/<int:uid>', userposts, name='userposts'),
    path('tag/<int:tid>', tag, name='tag'),
    path('login', Login, name='login'),
    path('register', Register, name='register'),
    path('logout', Logout, name='logout'),
    path('createpost', CreatePost, name='createpost'),
    path('updateblog/<int:bid>', UpdateBlog, name='updateblog'),
    path('deleteblog/<int:bid>', DeleteBlog, name='deleteblog'),
    path('likepost/<int:pid>', LikePost, name='like'),
    path('searchpost', SearchPost, name='searchpost'),
    path('updateProfile', UpdateProfile, name='updateprofile'),
    path('password_reset', PasswordReset, name="reset_password"),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('contact', contact, name='contact'),
    path('about', about, name='about'),
]