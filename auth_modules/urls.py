from django.urls import path
from .views import SignUpView,LoginView,LogoutView,success_view,MyProfilePageView,FollowUnfollowView,ProfilePageView


app_name = 'Authmodules'
urlpatterns = [
    path('signup',SignUpView.as_view(),name = "signup"),
    path('login',LoginView.as_view(),name = "login"),
    path('my_profile',MyProfilePageView.as_view(),name = "profile"),
    path('profile',ProfilePageView.as_view(),name = 'other_Profiles'),
    path('success',success_view, name='success-page'),
    path('logout',LogoutView.as_view(),name = "logout"),
    path('follow',FollowUnfollowView.as_view(),name = "follow"),
    
]
