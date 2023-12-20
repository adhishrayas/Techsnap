from django.urls import path
from .views import UploadMovieView,MovieLikeView,CreatePlayListView,ViewPlayListView,MovieDetailView,GetPlaylistsView,AddtoPlaylistView

urlpatterns = [
    path('upload_movie/',UploadMovieView.as_view(),name = 'upload_movie'),
    path('like_movies/',MovieLikeView.as_view(),name = 'like_unlike_movie'),
    path('create_playlist/',CreatePlayListView.as_view(),name = 'create_playlist'),
    path('view_playlist/',ViewPlayListView.as_view(),name = 'view_playlist'),
    path('movie_detail/',MovieDetailView.as_view(),name = 'about_movie'),
    path('get_playlists/',GetPlaylistsView.as_view(),name = 'get_playlists'),
    path('add_to_playlist/',AddtoPlaylistView.as_view(),name = 'add_to_playlist')
]
