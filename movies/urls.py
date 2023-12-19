from django.urls import path
from .views import UploadMovieView,MovieLikeView,CreatePlayListView,ViewPlayListView

urlpatterns = [
    path('upload_movie/',UploadMovieView.as_view(),name = 'upload_movie'),
    path('like_movies/',MovieLikeView.as_view(),name = 'like_unlike_movie'),
    path('create_playlist/',CreatePlayListView.as_view(),name = 'create_playlist'),
    path('view_playlist/',ViewPlayListView.as_view(),name = 'view_playlist')
]
