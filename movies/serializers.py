from rest_framework.serializers import ModelSerializer,ReadOnlyField,SerializerMethodField
from .models import Movies,Playlists,TrackObject
import requests
from django.conf import settings

class MovieSerializer(ModelSerializer):
    total_rating = ReadOnlyField()
    movie_photo = SerializerMethodField()
    
    class Meta:
        model = Movies
        fields = ("id","rating","rated_by","content_id","content_type","total_rating","movie_photo")
        extra_kwargs = {"id":{"read_only":True}}
    
    def get_movie_photo(self,obj):
        api_key = settings.API_KEY_TMDB
        content_type = obj.content_type
        content_id = obj.content_id
        if content_type == 'movie':
                tmdb_url = f'https://api.themoviedb.org/3/movie/{content_id}?api_key={api_key}&append_to_response=videos,credits'
                response = requests.get(tmdb_url)
                response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
                content_details = response.json()
                poster_path = content_details['poster_path']
                return f'https://image.tmdb.org/t/p/w500{poster_path}'
        else:  
                tmdb_url = f'https://api.themoviedb.org/3/tv/{content_id}?api_key={api_key}&append_to_response=videos,credits'
                response = requests.get(tmdb_url)
                response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
                content_details = response.json()
                poster_path = content_details['poster_path']
                return f'https://image.tmdb.org/t/p/w500{poster_path}'



class PlayListSerializer(ModelSerializer):
    movies = MovieSerializer(many = True,required = False)

    class Meta:
        model = Playlists
        fields = "__all__"
        extra_kwargs = {"id":{"read_only":True}}
    
    def create(self, validated_data):
        movies_data = validated_data.pop('movies', [])
        playlist = Playlists.objects.create(**validated_data)
        for movie_data in movies_data:
            movie = Movies.objects.get(**movie_data)
            playlist.movies.add(movie)
        return playlist

class PlaylistMiniSerializer(ModelSerializer):
    movie_count = SerializerMethodField()
    playlist_cover = SerializerMethodField()
    class Meta:
        model = Playlists
        fields = ("title","movie_count","playlist_cover","id")
    
    def get_movie_count(self,obj):
        return obj.movies.count()
    
    def get_playlist_cover(self,obj):
        movie = obj.movies.all().first()
        api_key = settings.API_KEY_TMDB
        if movie:
           content_type = movie.content_type
           content_id = movie.content_id
           if content_type == 'movie':
                tmdb_url = f'https://api.themoviedb.org/3/movie/{content_id}?api_key={api_key}&append_to_response=videos,credits'
                response = requests.get(tmdb_url)
                response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
                content_details = response.json()
                poster_path = content_details['poster_path']
                return f'https://image.tmdb.org/t/p/w500{poster_path}'
        else:
            return None

class TrackerSerializer(ModelSerializer):
    
    class Meta:
        model = TrackObject
        fields = "__all__"