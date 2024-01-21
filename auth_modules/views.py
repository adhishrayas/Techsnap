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
from movies.models import Playlists,CastObjects
# Create your views here.

class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)
    queryset= CustomUser.objects.all()

    def post(self,request,*args, **kwargs):
        if CustomUser.objects.filter(email = request.data.get('email')).exists():
            return render(request, 'account_exists.html')
        if CustomUser.objects.filter(username = request.data.get('username')).exists():
            return render(request, 'username_taken.html')
        serializer = SignUpSerializer(data = request.data)
        serializer.is_valid()
        user = serializer.save()
        try:
          token = Token.objects.create(user = user)
        except:
            user.delete()
            return render(request, 'unable_to_create_user.html')
        Playlists.objects.create(owner = user,title = "Seen",about = "All the movies that you have seen!")
        Playlists.objects.create(owner = user,title = "Must Watch",about = "Must Watch!!")
        Playlists.objects.create(owner = user,title = "Liked",about = "Your liked Movies!")
        Playlists.objects.create(owner = user,title = "DisLiked",about = "Your disliked movies")
        Playlists.objects.create(owner = user,title = "Tracking",about = "Movies you are Tracking!")
        login(request,user)
        token = Token.objects.get(user = user)
        user_data = SignUpSerializer(user)
        return Response({
            "token":token.key,
            "data":user_data.data
        }
        )
    

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self,request,*args, **kwargs):
        #try:
            user = CustomUser.objects.get(email = request.data.get('email'))
            if user.password == request.data.get('password'):
                token,_ = Token.objects.get_or_create(user = user)
                login(request,user)
                user_data = SignUpSerializer(user)
                return Response({
                    "message": "Logged in Successfully",
                    "token": token.key,
                    "user_data": user_data.data
                })
                # Render the success template with the payload data
              #  return render(request, 'loginsuccess.html', payload)
            else:
                return render(request, 'incorrect_credentials.html')
       # except:
        #        return render(request, 'user_not_found.html')

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
        return Response(context)
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
        
class EditProfileView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BasicProfileSerializer

    def post(self,request,*args, **kwargs):
        user = self.get_object()
        data = request.data.copy()
        if data['email']:
            user.email = data['email']
        if data['about']:
            user.about = data['about']
        if data.get('username'):
            user.username = data['username']
        if data['Phone_no']:
            user.Phone_no = data['Phone_no']
        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']
        user.save()
        return render(request,'updated.html')
    
    def get_object(self):
        return self.request.user
class search_users(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,*args, **kwargs):
        if 'query' in request.GET:
            query = request.GET['query']
            # Query the database for users with names similar to the entered query
            users = CustomUser.objects.filter(username__icontains=query)
            data = []
            for u in users:
                serializer = BasicProfileSerializer(u)
                data.append(serializer.data)
            #return render(request,'user_results.html',{"data":data})
            return Response({"data":data})
        else:
            return Response({"data":""})

    #return render(request, 'search_users.html', {'users': users})
        
class FollowingNotificationView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        user = self.request.user
        followers = UserFollowing.objects.filter(following_user_id = user)
        data = []
        for f in followers:
            obj = {}
            obj['follower'] = f.user_id.username
            obj['follower_id'] = f.user_id.id
            obj['followed_on'] = f.created
            data.append(obj)
        
        return render(request,'following_notifs.html',{"data":data})

class GetFollowersView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,*args, **kwargs):
        user = self.request.user
        followers = UserFollowing.objects.filter(following_user_id = user)
        data = []
        for f in followers:
            serializer = BasicProfileSerializer(f.user_id)
            data.append(serializer.data)
        return Response({"data":data})
        #return render(request,'user_results.html',{'data':data})
    
class GetFollowingView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,*args, **kwargs):
        user = self.request.user
        followers = UserFollowing.objects.filter(user_id = user)
        data = []
        for f in followers:
            serializer = BasicProfileSerializer(f.following_user_id)
            data.append(serializer.data)
        return Response({"data":data})
        return render(request,'user_results.html',{'data':data})
    
def settings_view(request):
    return render(request,'settings.html')

def success_view(request):
    return render(request, 'success.html')  

def search_users_view(request):
    return render(request,'searchu.html') 
        



