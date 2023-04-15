from django.db import models
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
import uuid
from datetime import datetime

User=get_user_model()

class Profile(models.Model):
    first_name=models.CharField(max_length=30 , blank=True)
    last_name=models.CharField(max_length=30 , blank=True)
    user =models.ForeignKey(User,on_delete=models.CASCADE)
#    user_id =models.IntegerField(primary_key=True)
    bio=models.TextField(blank=True)
    profile_pic=models.ImageField(upload_to='media/profile_images', default='media/default-profile-icon-24.jpg')
    location=models.CharField(max_length=100 , blank=True)


    def __dtr__(self):
        return self.user.username

class Post(models.Model):
    id =models.UUIDField(primary_key=True,default=uuid.uuid4)
    user =models.CharField(max_length=50)
#    user =models.ForeignKey(User,on_delete=models.CASCADE)
    postimg=models.ImageField(upload_to='media/post_images')
    postvid=models.ImageField(upload_to='media/post_video',blank=True)
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    likes=models.IntegerField(default=0)

class Like(models.Model):
    post_id=models.CharField(max_length=500)
    username=models.CharField(max_length=500)

    def __str__(self):
        return self.username

class Follower(models.Model):
    user=models.CharField(max_length=100)
    follower=models.CharField(max_length=100)

    def __str__(self):
        return self.user
