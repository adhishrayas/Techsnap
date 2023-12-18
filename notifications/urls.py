from django.urls import path
from .views import FeedView,PostLikeView,PostCreateView

urlpatterns = [
    path('feed',FeedView.as_view(),name = 'Feed'),
    path('create_post',PostCreateView.as_view(),name = 'Post Create'),
    path('Like_post',PostLikeView.as_view(),name = 'Like Post')
]
