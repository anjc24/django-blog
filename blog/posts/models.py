from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.



class User_Details(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    phone = models.TextField(max_length=10, null=True)
    image = models.FileField(null=True)
    about = models.TextField(null=True)

    def __str__(self):
        return self.usr.username

class Category(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    publishing_date = models.DateTimeField(auto_now_add= True)
    image = models.FileField(null=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name="post")
    tag = models.ManyToManyField(Tag, related_name="posts", blank=True)
    likecount = models.IntegerField(default=0)
    commentcount = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class LikeComment(models.Model):
    post_data = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    like = models.BooleanField(default=False)

    def __str__(self):
        return self.post_data.title

class Comment(models.Model):
    post_data = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    publishing_date = models.DateField(auto_now_add=True)



    def __str__(self):
        return self.post_data.title