from django.shortcuts import render
from django.db import transaction
from .models import MoviesLikes,Movies,Playlists,MoviesDisLikes,Ratings,Reaction,TrackObject
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

        context = {'api_response': {'results': results_with_images}}
        return render(request, 'see_more.html', context)
    else:
        return JsonResponse({'error': 'Failed to fetch data'})

class movie_details(APIView):
  
  permission_classes = (IsAuthenticated,)
  def get(self,request,*args, **kwargs):
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
        if "budget" in content_details:
            movie.budget = content_details["budget"]
        if "genres" in content_details:
            for g in content_details["genres"]:
              if "name" in g:
                movie.genre += g["name"] + ","
        if "original_language" in content_details:
            movie.language = content_details["original_language"]
        if "title" in content_details:
            movie.title = content_details["title"]
        if "overview" in content_details:
            movie.overview = content_details["overview"]
        if "release_date" in content_details:
            movie.release_date = content_details["release_date"]
        if "production_companies" in content_details:
            for p in content_details["production_companies"]:
              if "name" in p:
                movie.production_companies += p["name"] + ","
        if "revenue" in content_details:
            movie.revenue = content_details["revenue"]
        if "runtime" in content_details:
            movie.runtime = content_details["runtime"]
        if "status" in content_details:
            movie.status = content_details["status"]
        if "tagline" in content_details:
            movie.tagline = content_details["tagline"]
        if "videos" in content_details:
           if "results" in content_details["videos"]:
              results = content_details["videos"]["results"]
              if results:
                 movie.trailer_link = results[0]["key"]
        if "credits" in content_details:
            movie.cast_and_crew = content_details["credits"]
        movie.save()
        count = MoviesLikes.objects.filter(liked_on = movie).count()
        dis_like_count = MoviesDisLikes.objects.filter(liked_on = movie).count()
        rating,created = Ratings.objects.get_or_create(rated_by = self.request.user,rated_on = movie)
        reaction,created = Reaction.objects.get_or_create(reacted_by = self.request.user,reacted_on = movie)
        content_details['likes'] = count
        content_details['dislikes'] = dis_like_count
        content_details['rated'] = rating.rating
        content_details['reacted'] = reaction.reaction
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
                            episode['synopsis'] = episode_data.get('overview', '')  # Add episode synopsis
                            episode['episode_number'] = episode_number  # Add episode number
            
           # return Response({"data":content_details})
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
                    content_id=content_id, content_type=content_type
                )
                playlist = Playlists.objects.get(owner = self.request.user,title = "Liked")
                try:
                    like = MoviesLikes.objects.get(
                        liked_on=movie, liked_by=self.request.user
                    )
                    like.delete()
                    print("saved")
                    playlist.movies.add(movie)
                    playlist.save()
                    return Response({"Message": "Success"})
                except MoviesLikes.DoesNotExist:
                    playlist.movies.remove(movie)
                    playlist.save()
                    MoviesLikes.objects.create(liked_on=movie, liked_by=self.request.user)
                    return Response({"Message": "Success"})
        except Movies.DoesNotExist:
            return Response({"Message": "Movie not found"}, status=404)
        except Exception as e:
            return Response({"Message": f"An error occurred: {str(e)}"}, status=500)
        
class MovieDisLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        content_id = self.request.query_params.get('id')
        content_type = self.request.query_params.get('type')

        try:
            with transaction.atomic():
                movie, created = Movies.objects.get_or_create(
                    content_id=content_id, content_type=content_type
                )
                playlist = Playlists.objects.get(owner = self.request.user,title = "DisLiked")
                try:
                    Dislike = MoviesDisLikes.objects.get(
                        liked_on=movie, liked_by=self.request.user
                    )
                    Dislike.delete()
                    playlist.movies.remove(movie)
                    playlist.save()
                    return Response({"Message": "Success"})
                except MoviesDisLikes.DoesNotExist:
                    MoviesDisLikes.objects.create(liked_on=movie, liked_by=self.request.user)
                    playlist.movies.add(movie)
                    playlist.save()
                    return Response({"Message": "Success"})
        except Movies.DoesNotExist:
            return Response({"Message": "Movie not found"}, status=404)
        except Exception as e:
            return Response({"Message": f"An error occurred: {str(e)}"}, status=500)

class GetMovieLikesView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        type = self.request.query_params.get('type')
        movie = Movies.objects.get(content_id = id,content_type=type)
        count = MoviesLikes.objects.filter(liked_on = movie).count()
        return Response({"Likes":count})
    
class GetMovieDisLikesView(APIView):
    permission_classes=(IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        type = self.request.query_params.get('type')
        movie = Movies.objects.get(content_id = id,content_type=type)
        count = MoviesDisLikes.objects.filter(liked_on = movie).count()
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
        


class GetPlaylistsTemplateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        user = self.request.user
        excluded_titles = ['Seen','Liked','DisLiked','Tracking','Must Watch']
        playlists = Playlists.objects.filter(owner = user).exclude(title__in= excluded_titles)
        data = []
        for p in playlists:
            playlist_data = PlaylistMiniSerializer(p)
            data.append(playlist_data.data)
        return render(request,'my_playlists.html',{"data":data})
    
class GetPlaylistsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        user = self.request.user
        excluded_titles = ['Seen','Liked','DisLiked','Tracking','Must Watch']
        playlists = Playlists.objects.filter(owner = user).exclude(title__in= excluded_titles)
        data = []
        for p in playlists:
            playlist_data = PlaylistMiniSerializer(p)
            data.append(playlist_data.data)
        return Response({"data":data})
    
    
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

class GetYourPlayList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
      type = self.request.query_params.get('type')
      if type == "Tracking":
        user = self.request.user
        playlist = Playlists.objects.get(owner = user,title = type)
        serializer =PlayListSerializer(playlist)
        for movie in serializer.data['movies']:
                tracker = TrackObject.objects.get(content_id = movie['content_id'],owner = self.request.user)
                movie['episode_seen'] = tracker.episode
        #return Response({"data":serializer.data})
        return render(request,'playlist.html',{"data":serializer.data})
      else:
        user = self.request.user
        playlist = Playlists.objects.get(owner = user,title = type)
        serializer =PlayListSerializer(playlist)
        #return Response({"data":serializer.data})
        return render(request,'playlist.html',{"data":serializer.data})

class AddtoSeenPlaylistView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        movie_id = self.request.query_params.get('movie_id')
        type = self.request.query_params.get('type')
        try:
            movie = Movies.objects.get(content_id=movie_id,content_type = type)
            playlist = Playlists.objects.get(title = "Seen",owner = self.request.user)
            playlist.movies.add(movie)
            playlist.save()
            return Response({"message": "Added to playlist"})
        except Movies.DoesNotExist:
            return Response({"message": "Movie not found"}, status=400)
        except Playlists.DoesNotExist:
            return Response({"message": "Playlist not found"}, status=400)

class AddtoMustWatchPlaylistView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        movie_id = self.request.query_params.get('movie_id')
        type = self.request.query_params.get('type')
        try:
            movie = Movies.objects.get(content_id=movie_id,content_type = type)
            playlist = Playlists.objects.get(title = "Must Watch",owner = self.request.user)
            playlist.movies.add(movie)
            playlist.save()
            return Response({"message": "Added to playlist"})
        except Movies.DoesNotExist:
            return Response({"message": "Movie not found"}, status=400)
        except Playlists.DoesNotExist:
            return Response({"message": "Playlist not found"}, status=400)

class AddtoTrackingPlaylistView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        movie_id = self.request.query_params.get('movie_id')
        try:
            movie = Movies.objects.get(content_id=movie_id,content_type = "tv")
            playlist = Playlists.objects.get(title = "Tracking",owner = self.request.user)
            playlist.movies.add(movie)
            playlist.save()
            return Response({"message": "Added to playlist"})
        except Movies.DoesNotExist:
            return Response({"message": "Movie not found"}, status=400)
        except Playlists.DoesNotExist:
            return Response({"message": "Playlist not found"}, status=400)

class TrendingMediaView(APIView):
    def get(self, request, *args, **kwargs):
        api_key = settings.API_KEY_TMDB
        trending_movies_url = f'https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}'
        trending_series_url = f'https://api.themoviedb.org/3/trending/tv/week?api_key={api_key}'

        try:
            trending_movies_response = requests.get(trending_movies_url)
            trending_series_response = requests.get(trending_series_url)
            if trending_movies_response.status_code == 200 and trending_series_response.status_code == 200:
                trending_movies_data = trending_movies_response.json()
                trending_series_data = trending_series_response.json()
                trending_movies = [
                    {
                        'id':movie['id'],
                        'title': movie['title'],
                        'overview': movie['overview'],
                        'release_date': movie['release_date'],
                        'image_url': f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}",
                        'content_type':'movie',
                    }
                    for movie in trending_movies_data['results']
                ]

                trending_series = [
                    {
                        'id': series['id'],
                        'name': series['name'],
                        'overview': series['overview'],
                        'first_air_date': series['first_air_date'],
                        'image_url': f"https://image.tmdb.org/t/p/w500/{series['poster_path']}",
                        'content_type':'tv'
                    }
                    for series in trending_series_data['results']
                ]
                trending_media = {'trending_movies': trending_movies, 'trending_series': trending_series}
                return render(request,'trending.html',trending_media)
                return Response(trending_media)
            else:
                return Response({'error': 'Failed to fetch trending media'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpcomingReleaseView(APIView):
    def get(self, request, format=None):
        api_key = settings.API_KEY_TMDB  # Use settings module to access API key
        movie_url = f'https://api.themoviedb.org/3/movie/upcoming?api_key={api_key}&language=en-US&page=1'
        tv_url = f'https://api.themoviedb.org/3/tv/on_the_air?api_key={api_key}&language=en-US&page=1'

        try:
            movie_response = requests.get(movie_url)
            tv_response = requests.get(tv_url)

            movie_response.raise_for_status()
            tv_response.raise_for_status()

            movie_data = movie_response.json()
            tv_data = tv_response.json()

            movies = [
                {
                    'id': movie['id'],
                    'title': movie['title'],
                    'overview': movie['overview'],
                    'release_date': movie['release_date'],
                    'image_url': f"https://image.tmdb.org/t/p/w500/{movie['poster_path']}",
                    'content_type': 'movie',
                }
                for movie in movie_data.get('results', [])
            ]

            tv_shows = [
                {
                    'id': series['id'],
                    'name': series['name'],
                    'overview': series['overview'],
                    'first_air_date': series['first_air_date'],
                    'image_url': f"https://image.tmdb.org/t/p/w500/{series['poster_path']}",
                    'content_type': 'tv'
                }
                for series in tv_data.get('results', [])
            ]

            # Combine movie and TV show data
            results = {'movies': movies, 'tv_shows': tv_shows}
            return render(request,'upcoming.html',results)
        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RateMovieView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        content_id = self.request.query_params.get('id')
        content_type = self.request.query_params.get('type')
        Rating = self.request.query_params.get('rating')
        content = Movies.objects.get(content_id = content_id,content_type = content_type)
        rating = Ratings.objects.get(rated_by = self.request.user,rated_on = content)
        rating.rating = Rating
        rating.save()
        return Response({"message":"success"})
    
class ReactMovieView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        content_id = self.request.query_params.get('id')
        content_type = self.request.query_params.get('type')
        reacted = self.request.query_params.get('reaction')
        content = Movies.objects.get(content_id = content_id,content_type = content_type)
        reaction = Reaction.objects.get(reacted_by = self.request.user,reacted_on = content)
        reaction.reaction = reacted
        reaction.save()
        return Response({"message":"success"})

class AddTrackObjectView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        content_id = self.request.query_params.get('id')
        episode = self.request.query_params.get('ep')
        user = self.request.user
        track,created = TrackObject.objects.get_or_create(content_id = content_id,owner = user)
        track.episode = episode
        track.save()
        return Response({"message":"Success"})
