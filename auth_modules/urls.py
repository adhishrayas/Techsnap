from django.urls import path
from .views import SignUpView,LoginView,LogoutView,success_view


app_name = 'Authmodules'
urlpatterns = [
    path('signup',SignUpView.as_view(),name = "signup"),
    path('login',LoginView.as_view(),name = "login"),
    path('success/', success_view, name='success-page'),
    path('logout',LogoutView.as_view(),name = "logout"),
]
