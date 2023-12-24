from django.urls import path
from .views import (SignUpView,
                    LoginView,
                    LogoutView,
                    success_view,
                    FollowUnfollowView,
                    ProfilePageView,
                    EditProfileView,
                    search_users,
                    search_users_view,)


app_name = 'Authmodules'
urlpatterns = [
    path('signup',SignUpView.as_view(),name = "signup"),
    path('login',LoginView.as_view(),name = "login"),
    path('profile',ProfilePageView.as_view(),name = 'profiles'),
    path('success',success_view, name='success-page'),
    path('logout',LogoutView.as_view(),name = "logout"),
    path('follow',FollowUnfollowView.as_view(),name = "follow"),
    path('edit',EditProfileView.as_view(),name = "edit"),
    path('search',search_users_view,name = 'search'),
    path('results',search_users.as_view(),name = "results")
]
