from django.db import models
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User

User=get_user_model()

class Profile(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
#    user_id =models.IntegerField()
    bio=models.TextField(blank=True)
    profile_pic=models.ImageField(upload_to='media/profile_images', default='blank-profile-picture.jpg')
    location=models.CharField(max_length=100 , blank=True)


    def __dtr__(self):
        return self.user.username