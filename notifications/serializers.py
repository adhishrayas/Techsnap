from rest_framework.serializers import ModelSerializer,SerializerMethodField,ValidationError,FileField,CharField
from auth_modules.serializers import BasicProfileSerializer
from auth_modules.models import CustomUser
from .models import Notification,Likes,Stories,ReportedBlogs

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

class SeeStoriesSerializer(ModelSerializer):
    seen_by = SerializerMethodField()
    username = SerializerMethodField()
    class Meta:
        model = Stories
        fields = ("id","posted_by","created_at","media","caption","seen_by","username")
    
    def get_seen_by(self,obj):
        seen_users = obj.seen_by
        for s in self.instance:
          if s.posted_by == self.context['request'].user:
            return BasicProfileSerializer(seen_users,many = True).data
        return {}
    
    def get_username(self,obj):
       return obj.posted_by.username

class MaxLengthValidator:

    def __init__(self,max_duration = 15):
        self.max_duration = max_duration
    
    def __call__(self,value):
        if value and getattr(value,'duration',None) is not None:
            vid_duration = value.duration.total_seconds()
            if vid_duration > self.max_duration:
                return ValidationError(f'Video larger than {self.max_duration} cannot be uploaded!')

class CreateStorySerializer(ModelSerializer):
    media = FileField(validators=[MaxLengthValidator()])
    class Meta:
        model = Stories
        fields = ("media","caption")

class AddReportSerializer(ModelSerializer):

    class Meta:
        model = ReportedBlogs
        fields = ("report_sentence",)

class SeeIndividualStorySerializer(ModelSerializer):
    username = SerializerMethodField()
    class Meta:
        model = Stories
        fields = ("id","posted_by","created_at","media","caption","username")

    def get_username(self,obj):
       return obj.posted_by.username
