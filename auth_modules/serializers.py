from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import CustomUser,UserFollowing
from movies.serializers import MovieSerializer,PlayListSerializer,PlaylistMiniSerializer
from movies.models import MoviesLikes,Playlists

class SignUpSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("username","email","password","Phone_no","id")

class LoginSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("email","password",)

class FollowerSerializer(ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ("id","user_id","created")

class FollowingSerializer(ModelSerializer):

    class Meta:
        model = UserFollowing
        fields = ("id", "following_user_id", "created")

class BasicProfileSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("email","about","profile_pic","Phone_no","username")

class ProfileSerializer(ModelSerializer):
    following = SerializerMethodField()
    followers = SerializerMethodField()
    liked_movies = SerializerMethodField()
    playlists = SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ("id","email","about","profile_pic","Phone_no","username","following","followers","liked_movies","playlists")

    def get_following(self,obj):
        return obj.following.all().count()
    
    def get_followers(self,obj):
        return obj.followers.all().count()
    
    def get_liked_movies(self,obj):
        data = []
        try:
           liked_movies = MoviesLikes.objects.filter(liked_by = obj)
           for l in liked_movies:
               serializer = MovieSerializer(l.liked_on)
               data.append(serializer.data)
           return data
        except:
            return None
    
    def get_playlists(self,obj):
        data = []
        #try:
        playlists = Playlists.objects.filter(owner = obj)
        for p in playlists:
                serializer = PlaylistMiniSerializer(p)
                data.append(serializer.data)
        return data
        #except:
           # return None
