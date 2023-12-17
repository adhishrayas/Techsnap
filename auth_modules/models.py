import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key = True,
        editable = False,
        default = uuid.uuid4
    )
    username = models.CharField(max_length=255,blank=False,unique=True)
    password = models.CharField(max_length=255,blank=False)
    email = models.EmailField(blank=False)
    Phone_no = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.username
    

