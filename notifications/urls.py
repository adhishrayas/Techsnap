from django.urls import path
from .views import FeedView,PostLikeView,PostCreateView,GetLikesView,GetCommentsView

app_name = 'posts'
urlpatterns = [
    path('feed',FeedView.as_view(),name = 'Feed'),
    path('create_post',PostCreateView.as_view(),name = 'Post Create'),
    path('like_post',PostLikeView.as_view(),name = 'Like_Post'),
    path('get_Likes',GetLikesView.as_view(),name = 'Get_Likes'),
    path('get_comments',GetCommentsView.as_view(),name = 'Get_Comments')
]
