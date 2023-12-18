import uuid
from django.db import models
from auth_modules.models import CustomUser


class Notification(models.Model):
    id = models.UUIDField(
        primary_key = True,
        editable = False,
        default = uuid.uuid4
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name = "Sent_to")
    sent_by = models.ForeignKey(CustomUser,on_delete = models.CASCADE,related_name = "sent_by",null = True,blank = True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    button_name = models.CharField(max_length = 255)
    button_url = models.TextField()

    def __str__(self):
        return str(self.id)