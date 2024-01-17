from django.contrib import admin
from .models import Notification,Likes,ReportedBlogs,Stories
# Register your models here.
admin.site.register(Notification)
admin.site.register(Likes)
admin.site.register(ReportedBlogs)
admin.site.register(Stories)