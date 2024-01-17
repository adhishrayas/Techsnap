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
    parent_post = models.ForeignKey('self',on_delete = models.CASCADE,blank = True,null = True,related_name = 'replies')
    content_id = models.IntegerField(default = 0)
    content_type = models.CharField(max_length = 255,blank = True,null = True)
    def __str__(self):
        return self.user.username
    
    def is_reply(self):
        return self.parent_post is not None
    

class Likes(models.Model):
    id = models.UUIDField(
        primary_key = True,
        editable = False,
        default = uuid.uuid4
    )
    post_id = models.ForeignKey(Notification,on_delete = models.CASCADE)
    liked_by = models.ForeignKey(CustomUser,on_delete= models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add = True)
    seen = models.BooleanField(default = False)
    def __str__(self):
        return str(self.liked_by)
    
class Stories(models.Model):
    posted_by = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    media = models.FileField(upload_to = 'stories/',null = True,blank = True)
    caption = models.TextField(null = True,blank = True)
    seen_by = models.ManyToManyField(CustomUser,related_name='seen_by',null = True,blank=True)

    def __str__(self):
        return self.posted_by.username
    
class ReportedBlogs(models.Model):
    report_sentence = models.TextField(default = "")
    reported_by = models.ForeignKey(CustomUser,on_delete = models.DO_NOTHING)
    reported_on  = models.ForeignKey(Notification,on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add = True)

