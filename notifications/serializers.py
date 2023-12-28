from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import Notification,Likes


class PostSerializer(ModelSerializer):
    like = SerializerMethodField()
    user = SerializerMethodField()
    comments = SerializerMethodField()
    class Meta:
        model = Notification
        fields = ("id","user","content","timestamp","like","pic","parent_post","comments","content_id","content_type")
    
    def get_like(self,obj):
        return Likes.objects.filter(post_id = obj.id).count()
    def get_comments(self,obj):
        return Notification.objects.filter(parent_post = obj.id).count()
    def get_user(self, obj):
        user = obj.user 
        return user.username if user else None
    
class LikesSerializer(ModelSerializer):

    class Meta:
        model = Likes
        fields = "__all__"