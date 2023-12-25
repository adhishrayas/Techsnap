from django.urls import path
from .views import(
                   MovieLikeView,
                   CreatePlayListView,
                   ViewPlayListView,
                   GetPlaylistsView,
                   AddtoPlaylistView,
                   RemoveFromPlaylistView,
                   DeletePlayListView,
                   GetMovieLikesView,
                   search_movies,
                   search_results,
                   movie_details,
                   search_return)


app_name = "movies"
urlpatterns = [
    path('like_movies/',MovieLikeView.as_view(),name = 'like_unlike_movie'),
    path('create_playlist/',CreatePlayListView.as_view(),name = 'create_playlist'),
    path('remove_playlist/',DeletePlayListView.as_view(),name = 'delete_playlist'),
    path('view_playlist/',ViewPlayListView.as_view(),name = 'view_playlist'),
    path('get_playlists/',GetPlaylistsView.as_view(),name = 'get_playlists'),
    path('get_movie_likes/',GetMovieLikesView.as_view(),name = "get_likes"),
    path('add_to_playlist/',AddtoPlaylistView.as_view(),name = 'add_to_playlist'),
    path('remove_from_playlist/',RemoveFromPlaylistView.as_view(),name = 'remove_from_playlist'),
    path('search/', search_movies, name='search_movies'),
    path('search_results/',search_results, name='search_results'),
    path('movie-details/',movie_details,name='movie_details'),
    path('movie-search-results',search_return,name = 'results')
]
