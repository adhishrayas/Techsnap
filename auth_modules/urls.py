from django.urls import path
from .views import SignUpView,LoginView,LogoutView,success_view,FollowUnfollowView,ProfilePageView


app_name = 'Authmodules'
urlpatterns = [
    path('signup',SignUpView.as_view(),name = "signup"),
    path('login',LoginView.as_view(),name = "login"),
    path('profile',ProfilePageView.as_view(),name = 'profiles'),
    path('success',success_view, name='success-page'),
    path('logout',LogoutView.as_view(),name = "logout"),
    path('follow',FollowUnfollowView.as_view(),name = "follow"),
]
