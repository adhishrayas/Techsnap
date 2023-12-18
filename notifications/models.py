import uuid
from django.db import models
from auth_modules.models import CustomUser


class Notification(models.Model):
    id = models.UUIDField(
        primary_key = True,
        editable = False,
        default = uuid.uuid4
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null = True)
    content = models.TextField()
    pic = models.ImageField(upload_to='posts/',null = True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Likes(models.Model):
    id = models.UUIDField(
        primary_key = True,
        editable = False,
        default = uuid.uuid4
    )
    post_id = models.ForeignKey(Notification,on_delete = models.CASCADE)
    liked_by = models.ForeignKey(CustomUser,on_delete= models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.liked_by)
