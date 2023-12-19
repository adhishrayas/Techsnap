from rest_framework.serializers import ModelSerializer,ReadOnlyField
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