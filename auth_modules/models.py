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
    about = models.TextField(blank = True,null = True)
    profile_pic = models.ImageField(blank=True,null=True,upload_to='profile/')
    Phone_no = models.IntegerField(blank=True,null=True)
    is_uploader = models.BooleanField(default = False)
    def __str__(self):
        return self.username
    
class UserFollowing(models.Model):
    user_id = models.ForeignKey(CustomUser, related_name="following",on_delete = models.CASCADE)
    following_user_id = models.ForeignKey(CustomUser, related_name="followers",on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]
        ordering = ["-created"]

    def __str__(self):
        f"{self.user_id} follows {self.following_user_id}"