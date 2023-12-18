from rest_framework.serializers import ModelSerializer,SerializerMethodField,SlugRelatedField
from .models import Notification,Likes
from auth_modules.models import CustomUser

class PostSerializer(ModelSerializer):
    like = SerializerMethodField()
    user = SerializerMethodField()
    class Meta:
        model = Notification
        fields = ("id","user","content","timestamp","like")
    
    def get_like(self,obj):
        return Likes.objects.filter(post_id = obj.id).count()
    def get_user(self, obj):
        user = obj.user  # Assuming 'user' is a ForeignKey in the Notification model
        return user.username if user else None