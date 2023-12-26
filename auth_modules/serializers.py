import requests
from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import CustomUser,UserFollowing
from movies.serializers import PlaylistMiniSerializer
from movies.models import MoviesLikes,Playlists
from django.conf import settings

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
        fields = ("email","about","profile_pic","Phone_no","username","id")

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
        api_key = settings.API_KEY_TMDB
        liked_movies = MoviesLikes.objects.filter(liked_by = obj)
        for l in liked_movies:
               content_type = l.liked_on.content_type
               content_id = l.liked_on.content_id
               tmdb_url = f'https://api.themoviedb.org/3/{content_type}/{content_id}?api_key={api_key}&append_to_response=videos,credits'
               response = requests.get(tmdb_url)
               response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
               content_details = response.json()
               content_details['type'] = content_type
               data.append(content_details)
        return data
        #except:
        #    print("yo")
        #    return None
    
    def get_playlists(self,obj):
        data = []
        #try:
        excluded_titles = ['Seen','Liked','DisLiked','Tracking','Must Watch']
        playlists = Playlists.objects.filter(owner = obj,is_private=False).exclude(title__in = excluded_titles)
        for p in playlists:
                serializer = PlaylistMiniSerializer(p)
                data.append(serializer.data)
        return data
        #except:
           # return None
