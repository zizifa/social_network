from django.db import models
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
import uuid
from datetime import datetime

User=get_user_model()

class Profile(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
#    user_id =models.IntegerField()
    bio=models.TextField(blank=True)
    profile_pic=models.ImageField(upload_to='media/profile_images', default='profile_default.png')
    location=models.CharField(max_length=100 , blank=True)


    def __dtr__(self):
        return self.user.username

class Post(models.Model):
    id =models.UUIDField(primary_key=True,default=uuid.uuid4)
    user =models.CharField(max_length=50)
#    user =models.ForeignKey(User,on_delete=models.CASCADE)
    postimg=models.ImageField(upload_to='media/post_images',default='media/default.png')
    caption=models.TextField()
    created_at=models.DateTimeField(default=datetime.now)
    likes=models.IntegerField(default=0)

class Like(models.Model):
    post_id=models.CharField(max_length=500)
    username=models.CharField(max_length=500)

    def __str__(self):
        return self.username