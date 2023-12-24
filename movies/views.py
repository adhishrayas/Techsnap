from django.shortcuts import render
from .models import MoviesLikes,Movies,Playlists
from .serializers import MovieSerializer,PlayListSerializer,MovieBriefSerializer,PlaylistMiniSerializer
from auth_modules.models import UserFollowing
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,CreateAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from auth_modules.permissions import IsAuthorOrReadOnly
from django.http import JsonResponse
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
            results_with_images.append(result)
        for result in results_tv_shows:
            poster_path = result.get('poster_path')
            if poster_path:
                result['poster_url'] = f'https://image.tmdb.org/t/p/w500{poster_path}'
            else:
                result['poster_url'] = None
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
            results_with_images.append(result)

        for result in results_tv_shows:
            poster_path = result.get('poster_path')
            if poster_path:
                result['poster_url'] = f'https://image.tmdb.org/t/p/w500{poster_path}'
            else:
                result['poster_url'] = None
            results_with_images.append(result)

        context = {'results': results_with_images, 'query': query}
        return render(request, 'see_more.html', context)
    else:
        return JsonResponse({'error': 'Failed to fetch data'})
    

def movie_details(request, movie_id):
    api_key = settings.API_KEY_TMDB
    tmdb_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=videos,credits'

    try:
        response = requests.get(tmdb_url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        movie_details = response.json()
    except requests.exceptions.RequestException as e:
        # Handle API request errors, you might want to log the error or show an error page
        return render(request, 'error.html', {'error_message': f'Error fetching movie details: {str(e)}'})

    # Pass movie details to the template
    return render(request, 'movie_details.html', {'content_details': movie_details})


class UploadMovieView(CreateAPIView):
    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        user = self.request.user
        if user.is_uploader:
            return Response({"message":"Upload your Movie"},status = status.HTTP_200_OK)
        else:
            return Response({"message":"Not Authorized"},status=status.HTTP_401_UNAUTHORIZED)
        
    def perform_create(self, serializer):
        serializer.save(uploaded_by = self.request.user)

class MovieLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        movie = Movies.objects.get(id = id)
        try:
          like = MoviesLikes.objects.get(liked_on= movie,liked_by = self.request.user)
          like.delete()
          return Response({"Message":"Unliked"})
        except:
          MoviesLikes.objects.create(liked_on = movie,liked_by = self.request.user)
          return Response({"Message":"Liked"})
  
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
        
class MovieDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        movie = Movies.objects.get(id = id)
        movie.views += 1
        movie.save()
        serializer = MovieSerializer(movie)
        return render(request,'movie_detail.html',{"data":serializer.data})
        return Response({"data":serializer.data},status=status.HTTP_200_OK)

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
        playlist_id = self.request.query_params.get('playlist_id')

        try:
            movie = Movies.objects.get(id=movie_id)
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
        

class GetAllMovies(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        data = []
        for m in Movies.objects.all():
            serializer = MovieBriefSerializer(m)
            data.append(serializer.data)
        return Response({"data":data})
    