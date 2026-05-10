from django.db import models
from django.contrib.auth.models import AbstractUser

class user(AbstractUser):
        email=models.EmailField(max_length=255,unique=True)
        name=models.CharField(max_length=255, unique=True)
        avatar_url=models.URLField(max_length=200,blank=True,null=True)

        provider=models.CharField(max_length=255,blank=True,null=True)
        provider_user_id=models.CharField(max_length=50,blank=True,null=True)

        USERNAME_FIELD ='email'
        REQUIRED_FIELDS=['username']
        def __str__(self):
           return self.email
    
