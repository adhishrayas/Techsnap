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
                   search_return,
                   GetPlaylistsTemplateView,
                   GetYourPlayList,
                   GetMovieDisLikesView,
                   MovieDisLikeView,
                   AddtoSeenPlaylistView,
                   AddtoMustWatchPlaylistView,
                   AddtoTrackingPlaylistView,
                   TrendingMediaView,
                   UpcomingReleaseView,
                   ReactMovieView,
                   RateMovieView,
                   AddTrackObjectView,
                   GetVideosView
                   )


app_name = "movies"
urlpatterns = [
    path('like_movies/',MovieLikeView.as_view(),name = 'like_unlike_movie'),
    path('create_playlist/',CreatePlayListView.as_view(),name = 'create_playlist'),
    path('remove_playlist/',DeletePlayListView.as_view(),name = 'delete_playlist'),
    path('view_playlist/',ViewPlayListView.as_view(),name = 'view_playlist'),
    path('get_playlists/',GetPlaylistsView.as_view(),name = 'get_playlists'),
    path('your_playlists/',GetPlaylistsTemplateView.as_view(),name = 'my_playlists'),
    path('get_movie_likes/',GetMovieLikesView.as_view(),name = "get_likes"),
    path('add_to_playlist/',AddtoPlaylistView.as_view(),name = 'add_to_playlist'),
    path('remove_from_playlist/',RemoveFromPlaylistView.as_view(),name = 'remove_from_playlist'),
    path('search/', search_movies, name='search_movies'),
    path('search_results/',search_results, name='search_results'),
    path('movie-details/',movie_details.as_view(),name='movie_details'),
    path('movie-search-results',search_return,name = 'results'),
    path('your_playlist/',GetYourPlayList.as_view(),name = "your_playlist"),
    path('get_dislikes/',GetMovieDisLikesView.as_view(),name = "dislikes_count"),
    path('dislike_movie/',MovieDisLikeView.as_view(),name = "Dislike"),
    path('add_to_scene/',AddtoSeenPlaylistView.as_view(),name = "Add_scene"),
    path('add_to_must/',AddtoMustWatchPlaylistView.as_view(),name = "Add_must"),
    path('add_to_track/',AddtoTrackingPlaylistView.as_view(),name = "Add_tracking"),
    path('trending/',TrendingMediaView.as_view(),name = "Trending"),
    path('upcoming/',UpcomingReleaseView.as_view(),name = "Upcoming"),
    path('rate/',RateMovieView.as_view(),name = "rate"),
    path('react/',ReactMovieView.as_view(),name = "react"),
    path('track/',AddTrackObjectView.as_view(),name = "track"),
    path('videos/',GetVideosView.as_view(),name = "videos")
]
