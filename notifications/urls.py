from django.urls import path
from .views import (
    FeedView,
    PostLikeView,
    PostCreateView,
    GetLikesView,
    GetCommentsView,
    PostDetailView,
    UnseenLikesView,
    CommentsNotifsView,
    MovieFeedView,
    SeeStoryView,
    GetAllStoriesView,
    CreateStoryView,
    AddReportView
    )

app_name = 'posts'
urlpatterns = [
    path('feed',FeedView.as_view(),name = 'Feed'),
    path('create_post',PostCreateView.as_view(),name = 'Post Create'),
    path('like_post',PostLikeView.as_view(),name = 'Like_Post'),
    path('get_Likes',GetLikesView.as_view(),name = 'Get_Likes'),
    path('get_comments',GetCommentsView.as_view(),name = 'Get_Comments'),
    path('get_details/',PostDetailView.as_view(),name='post_detail'),
    path('unseen_likes/',UnseenLikesView.as_view(),name = 'unseen_likes'),
    path('comments/',CommentsNotifsView.as_view(),name = 'comments_notifs'),
    path('movie_feed/',MovieFeedView.as_view(),name = 'movie_feed'),
    path('see_story/<int:story_id>/',SeeStoryView.as_view(),name = 'see_story'),
    path('get_stories',GetAllStoriesView.as_view(),name = 'get_stories'),
    path('create_story/',CreateStoryView.as_view(),name = 'create_story'),
    path('add_report/<uuid:post_id>',AddReportView.as_view(),name = 'add_report')
]
