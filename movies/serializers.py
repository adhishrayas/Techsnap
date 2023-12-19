from rest_framework.serializers import ModelSerializer,ReadOnlyField,SerializerMethodField
from .models import Movies,Playlists


class MovieSerializer(ModelSerializer):
    total_rating = ReadOnlyField()
    class Meta:
        model = Movies
        fields = "__all__"
        extra_kwargs = {"id":{"read_only":True}}

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
        fields = ("title","movie_count","playlist_cover")
    
    def get_movie_count(self,obj):
        return obj.movies.count()
    
    def get_playlist_cover(self,obj):
        movie = obj.movies.all().first()
        if movie:
           return movie.movie_file
        else:
            return None
