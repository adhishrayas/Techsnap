from django.shortcuts import render
from .models import MoviesLikes,Movies,Playlists
from .serializers import MovieSerializer,PlayListSerializer,MovieBriefSerializer
from auth_modules.models import UserFollowing
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,CreateAPIView
from rest_framework.permissions import IsAuthenticated


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
        except:
          MoviesLikes.objects.create(liked_on = movie,liked_by = self.request.user)
        return Response({"Message":"Succesfull"})
  
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
        headers = self.get_success_headers(serializer.data)
        context = {"data":serializer.data}
        return render(request,'playlist.html',context)

    def perform_create(self, serializer):
        serializer.save()

class ViewPlayListView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PlayListSerializer

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        playlist = Playlists.objects.get(id = id)
        if playlist.owner == self.request.user:
            serializer = PlayListSerializer(playlist)
            context = {"data": serializer.data}
            return render(request, 'playlist.html', context)
        if playlist.is_private:
            user = self.request.user
            owner = playlist.owner
            try:
               followed = UserFollowing.objects.get(user_id = user,following_user_id = owner)
               serializer = PlayListSerializer(playlist)
               context = {"data": serializer.data}
               return render(request, 'playlist.html', context)
            except:
                return Response({"message":"This Playlist is Private"},status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = PlayListSerializer(playlist)
            context = {"data": serializer.data}
            return render(request, 'playlist.html', context)
        
class MovieDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        movie = Movies.objects.get(id = id)
        movie.views += 1
        movie.save()
        serializer = MovieSerializer(movie)
        return Response({"data":serializer.data},status=status.HTTP_200_OK)

class GetPlaylistsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        user = self.request.user
        playlists = Playlists.objects.filter(owner = user)
        data = []
        for p in playlists:
            playlist_data = PlayListSerializer(p)
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

            playlist.movies.add(movie)
            playlist.save()

            return Response({"message": "Added to playlist"})
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

            playlist.movies.remove(movie)
            playlist.save()
            return Response({"message": "Removed from playlist"})
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