from django.shortcuts import render
from django.db import transaction
from .models import MoviesLikes,Movies,Playlists
from .serializers import PlayListSerializer,PlaylistMiniSerializer
from auth_modules.models import UserFollowing
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,CreateAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from auth_modules.permissions import IsAuthorOrReadOnly
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings
import requests

def search_movies(request):
    return render(request, 'search.html')

def search_results(request):
    query = request.GET.get('query')
    api_key = settings.API_KEY_TMDB
    base_url_movies = 'https://api.themoviedb.org/3/search/movie'
    base_url_tv_shows = 'https://api.themoviedb.org/3/search/tv'
    params = {'api_key': api_key, 'query': query}
    
    # Fetch movie results
    response_movies = requests.get(base_url_movies, params=params)
    data_movies = response_movies.json()
    
    # Fetch TV show results
    response_tv_shows = requests.get(base_url_tv_shows, params=params)
    data_tv_shows = response_tv_shows.json()

    if response_movies.status_code == 200 and response_tv_shows.status_code == 200:
        results_movies = data_movies.get('results', [])
        results_tv_shows = data_tv_shows.get('results', [])
        results_with_images = []

        # Add content type to movie results
        for result in results_movies:
            poster_path = result.get('poster_path')
            if poster_path:
                result['poster_url'] = f'https://image.tmdb.org/t/p/w500{poster_path}'
            else:
                result['poster_url'] = None
            result['content_type'] = 'movie'
            results_with_images.append(result)

        # Add content type to TV show results
        for result in results_tv_shows:
            poster_path = result.get('poster_path')
            if poster_path:
               result['poster_url'] = f'https://image.tmdb.org/t/p/w500{poster_path}'
            else:
               result['poster_url'] = None
            result['content_type'] = 'tv'
            result['title'] = result.get('name', '')  # Use 'name' instead of 'title' for TV shows
            results_with_images.append(result)

        return JsonResponse({'results': results_with_images})
    else:
        return JsonResponse({'error': 'Failed to fetch data'})

def search_return(request):
    query = request.GET.get('query')
    api_key = settings.API_KEY_TMDB
    base_url_movies = 'https://api.themoviedb.org/3/search/movie'
    base_url_tv_shows = 'https://api.themoviedb.org/3/search/tv'
    params = {'api_key': api_key, 'query': query}
    response_movies = requests.get(base_url_movies, params=params)
    data_movies = response_movies.json()
    response_tv_shows = requests.get(base_url_tv_shows, params=params)
    data_tv_shows = response_tv_shows.json()

    if response_movies.status_code == 200 and response_tv_shows.status_code == 200:
        results_movies = data_movies.get('results', [])
        results_tv_shows = data_tv_shows.get('results', [])
        results_with_images = []

        for result in results_movies:
            poster_path = result.get('poster_path')
            if poster_path:
                result['poster_url'] = f'https://image.tmdb.org/t/p/w500{poster_path}'
            else:
                result['poster_url'] = None
            result['content_type'] = 'movie'
            results_with_images.append(result)

        for result in results_tv_shows:
            poster_path = result.get('poster_path')
            if poster_path:
                result['poster_url'] = f'https://image.tmdb.org/t/p/w500{poster_path}'
            else:
                result['poster_url'] = None
            result['content_type'] = 'tv'
            results_with_images.append(result)

        context = {'results': results_with_images, 'query': query}
        return render(request, 'see_more.html', context)
    else:
        return JsonResponse({'error': 'Failed to fetch data'})
    

@api_view(['GET'])
def movie_details(request):
    api_key = settings.API_KEY_TMDB
    content_type = request.GET.get('type')
    content_id = request.GET.get('id')
    
    if content_type == 'movie':
        tmdb_url = f'https://api.themoviedb.org/3/movie/{content_id}?api_key={api_key}&append_to_response=videos,credits'
    elif content_type == 'tv':
        tmdb_url = f'https://api.themoviedb.org/3/tv/{content_id}?api_key={api_key}&append_to_response=videos,credits'
    else:
        return Response({'error_message': 'Invalid content type'})
    
    try:
        response = requests.get(tmdb_url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        content_details = response.json()
        movie,created = Movies.objects.get_or_create(content_id = content_id,content_type = content_type)
        count = MoviesLikes.objects.filter(liked_on = movie).count()
        content_details['likes'] = count
        if content_type == 'tv':
            # Add videos for each episode
            for season in content_details.get('seasons', []):
                season_number = season.get('season_number')
                if season_number is not None:
                    season_url = f'https://api.themoviedb.org/3/tv/{content_id}/season/{season_number}?api_key={api_key}&append_to_response=videos'
                    season_response = requests.get(season_url)
                    season_response.raise_for_status()
                    season_data = season_response.json()
                    season['episodes'] = season_data.get('episodes', [])

                     # Add videos for each episode
                    for episode in season['episodes']:
                        episode_number = episode.get('episode_number')
                        if episode_number is not None:
                            episode_url = f'https://api.themoviedb.org/3/tv/{content_id}/season/{season_number}/episode/{episode_number}?api_key={api_key}&append_to_response=videos'
                            episode_response = requests.get(episode_url)
                            episode_response.raise_for_status()
                            episode_data = episode_response.json()
                            episode['videos'] = episode_data.get('videos', {})
                            
            return render(request, 'series.html', {'content_details': content_details})
    except requests.exceptions.RequestException as e:
        # Handle API request errors, you might want to log the error or show an error page
        return Response({'error_message': f'Error fetching content details: {str(e)}'})
    #return Response({'content_details':content_details})
    return render(request,'movie_details.html',{'content_details': content_details})

class MovieLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        content_id = self.request.query_params.get('id')
        content_type = self.request.query_params.get('type')

        try:
            with transaction.atomic():
                movie, created = Movies.objects.get_or_create(
                    content_id=content_id, content_type="movie"
                )

                try:
                    like = MoviesLikes.objects.get(
                        liked_on=movie, liked_by=self.request.user
                    )
                    like.delete()
                    return Response({"Message": "Success"})
                except MoviesLikes.DoesNotExist:
                    MoviesLikes.objects.create(liked_on=movie, liked_by=self.request.user)
                    return Response({"Message": "Success"})
        except Movies.DoesNotExist:
            return Response({"Message": "Movie not found"}, status=404)
        except Exception as e:
            return Response({"Message": f"An error occurred: {str(e)}"}, status=500)

class GetMovieLikesView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        movie = Movies.objects.get(content_id = id)
        count = MoviesLikes.objects.filter(liked_on = movie).count()
        return Response({"Likes":count})

class CreatePlayListView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlayListSerializer

    def get(self,request,*args, **kwargs):
        return render(request,'create_playlist.html')
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        context = {"data":serializer.data}
        print(context)
        return Response(context)

    def perform_create(self, serializer):
        serializer.save()

class DeletePlayListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        playlist = Playlists.objects.get(id = id)
        playlist.delete()
        return Response({"message":"Deleted"})
    
class ViewPlayListView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlayListSerializer

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        playlist = Playlists.objects.get(id = id)
        if playlist.owner == self.request.user:
            serializer = PlayListSerializer(playlist)
            context = {"data": serializer.data,
                       "is_owner":True}
            return render(request, 'playlist.html', context)
        if playlist.is_private:
            user = self.request.user
            owner = playlist.owner
            try:
               followed = UserFollowing.objects.get(user_id = user,following_user_id = owner)
               serializer = PlayListSerializer(playlist)
               context = {"data": serializer.data,
                          "is_owner":False}
               return render(request, 'playlist.html', context)
            except:
                return Response({"message":"This Playlist is Private"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = PlayListSerializer(playlist)
            context = {"data": serializer.data,
                       "is_owner":False}
            return render(request, 'playlist.html', context)
        


class GetPlaylistsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        user = self.request.user
        playlists = Playlists.objects.filter(owner = user)
        data = []
        for p in playlists:
            playlist_data = PlaylistMiniSerializer(p)
            data.append(playlist_data.data)
        return Response({"data":data},status=status.HTTP_200_OK)
    
class AddtoPlaylistView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        movie_id = self.request.query_params.get('movie_id')
        type = self.request.query_params.get('type')
        playlist_id = self.request.query_params.get('playlist_id')
        try:
            movie = Movies.objects.get(content_id=movie_id,content_type = type)
            playlist = Playlists.objects.get(id=playlist_id)
            if playlist.owner == self.request.user:
              playlist.movies.add(movie)
              playlist.save()
              return Response({"message": "Added to playlist"})
            else:
              return Response({"message":"Not Authorized"})
        except Movies.DoesNotExist:
            return Response({"message": "Movie not found"}, status=400)
        except Playlists.DoesNotExist:
            return Response({"message": "Playlist not found"}, status=400)

class RemoveFromPlaylistView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        movie_id = self.request.query_params.get('movie_id')
        playlist_id = self.request.query_params.get('playlist_id')
        try:
            movie = Movies.objects.get(id=movie_id)
            playlist = Playlists.objects.get(id=playlist_id)
            if playlist.owner == self.request.user:
                playlist.movies.remove(movie)
                playlist.save()
                return Response({"message": "Removed from playlist"})
            else:
                return Response({"message":"Not authorized"})
        except Movies.DoesNotExist:
            return Response({"message": "Movie not found"}, status=400)
        except Playlists.DoesNotExist:
            return Response({"message": "Playlist not found"}, status=400)
        

