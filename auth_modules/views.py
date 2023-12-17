from django.shortcuts import render
from django.contrib.auth import login,logout
from .serializers import SignUpSerializer,LoginSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import CustomUser
# Create your views here.

class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)
    queryset= CustomUser.objects.all()

    def post(self,request,*args, **kwargs):
        if CustomUser.objects.filter(email = request.data.get('email')).exists():
            return Response({"message":"Account with this email already exists"},status = status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(username = request.data.get('username')).exists():
            return Response({"message":"This username is taken"},status = status.HTTP_400_BAD_REQUEST)
        serializer = SignUpSerializer(data = request.data)
        serializer.is_valid()
        serializer.save()
        user = serializer.instance
        try:
          token = Token.objects.create(user = user)
        except:
            user.delete()
            return Response({"message":"Unable to create user"},status = status.HTTP_400_BAD_REQUEST)
        login(request,user)
        token = Token.objects.get(user = user)
        user_data = SignUpSerializer(user)
        return Response({"message":"Account created succesfully !","token":token.key,"user_info":user_data.data},status = status.HTTP_201_CREATED)
    

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.all()

    def post(self,request,*args, **kwargs):
        try:
            user = CustomUser.objects.get(email = request.data.get('email'))
            if user.password == request.data.get('password'):
                token,_ = Token.objects.get_or_create(user = user)
                login(request,user)
                user_data = SignUpSerializer(user)
                return Response({"message":"Logged in Succesfully","token":token.key,"user_data":user_data.data},status = status.HTTP_200_OK)
            else:
                return Response({"message":"Please use correct credentials"},status = status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"User not found"},status = status.HTTP_404_NOT_FOUND)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
      try:
        user = self.request.user
        token = Token.objects.get(user = user)
        logout(request)
        token.delete()
        return Response({"message":"Logged out succesfully"},status = status.HTTP_200_OK)
      except:
        return Response({"message":"Unable to log out"},status = status.HTTP_400_BAD_REQUEST)



            
        





