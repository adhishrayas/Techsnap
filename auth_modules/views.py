from django.shortcuts import render,get_object_or_404
from django.contrib.auth import login,logout
from .serializers import SignUpSerializer,LoginSerializer,ProfileSerializer,BasicProfileSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from .models import CustomUser,UserFollowing
# Create your views here.

class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)
    queryset= CustomUser.objects.all()
    def get(self, request, *args, **kwargs):
        default_values = {
            "username": "",
            "email": "",
            "phone": None,
        }
        return render(request, 'signup.html', default_values)
    def post(self,request,*args, **kwargs):
        if CustomUser.objects.filter(email = request.data.get('email')).exists():
            return render(request, 'account_exists.html')
        if CustomUser.objects.filter(username = request.data.get('username')).exists():
            return render(request, 'username_taken.html')
        serializer = SignUpSerializer(data = request.data)
        serializer.is_valid()
        serializer.save()
        user = serializer.instance
        try:
          token = Token.objects.create(user = user)
        except:
            user.delete()
            return render(request, 'unable_to_create_user.html')
        login(request,user)
        token = Token.objects.get(user = user)
        user_data = SignUpSerializer(user)
        return render(request, 'account_created.html',user_data.data)
    

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {'email': '', 'password': ''})
    def post(self,request,*args, **kwargs):
        try:
            user = CustomUser.objects.get(email = request.data.get('email'))
            if user.password == request.data.get('password'):
                token,_ = Token.objects.get_or_create(user = user)
                login(request,user)
                user_data = SignUpSerializer(user)
                payload = {
                    "message": "Logged in Successfully",
                    "token": token.key,
                    "user_data": user_data.data
                }
                #return Response({"data":payload})
                # Render the success template with the payload data
                return render(request, 'loginsuccess.html', payload)
            else:
                return render(request, 'incorrect_credentials.html')
        except:
                return render(request, 'user_not_found.html')

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
      try:
        user = self.request.user
        token = Token.objects.get(user = user)
        logout(request)
        message = "Logged out successfully"
        return render(request, 'logout_view.html', {'message': message})
      except:
        message = "Unable to log out"
        return render(request, 'logout_view.html', {'message': message})


class MyProfilePageView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user
    
    def get(self,request,*args, **kwargs):
        user = self.request.user
        serializer = ProfileSerializer(user)
        #return Response({"data":serializer.data})
        return render(request, 'my_profile.html', {"data":serializer.data})
    
class ProfilePageView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
       try:
           id = self.request.query_params.get('id')
           return get_object_or_404(CustomUser, id=id)
       except:
           return self.request.user
       
    def get(self,request,*args, **kwargs):
        user = self.get_object()
        serializer = ProfileSerializer(user)
        self_user = self.request.user

        #return Response({"data":serializer.data})
        context = {
        'data': serializer.data,
        'is_owner': user == self_user,
    }
        print(user == self_user)#dont know how this made it work, but dont remove this line or it breaks
        #return Response(context)
        return render(request, 'my_profile.html',context)
    
class FollowUnfollowView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        user = self.request.user
        id = self.request.query_params.get('id')
        following = CustomUser.objects.get(id = id)
        try:
            follow_obj = UserFollowing.objects.get(user_id = user,following_user_id = following)
            follow_obj.delete()
            return Response({"message":"Unfollowed"},status=status.HTTP_200_OK)
        except:
            follow_obj = UserFollowing.objects.create(user_id = user,following_user_id = following)
            return Response({"message":"Followed"},status = status.HTTP_200_OK)

def success_view(request):
    return render(request, 'success.html')   
        



