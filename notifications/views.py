from django.shortcuts import render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import BasePermission,IsAuthenticated
from .models import Notification
from .serializers import CreateNotificationSerializer,GetNotificationSerializer

# Create your views here.

class SuperUserAuthenticationPermission(BasePermission):

    def has_permission(self,request,view):
        user = request.user
        if user and user.is_authenticated:
            return user.is_superuser
        return False
        
class CreateNotificationView(GenericAPIView):
    serializer_class = CreateNotificationSerializer
    permission_classes = (IsAuthenticated,SuperUserAuthenticationPermission)
    queryset = Notification.objects.all()

    def post(self,request,*args, **kwargs):
      try:
        mutabale_data = request.data.copy()
        mutabale_data['sent_by'] = self.request.user.id
        serializer = CreateNotificationSerializer(data = mutabale_data)
        serializer.is_valid()
        serializer.save(sent_by=self.request.user)
        message = serializer.instance
        message_data = CreateNotificationSerializer(message)
        return Response({"message":"Notification has been sent","Data":message_data.data},status = status.HTTP_201_CREATED)
      except:
        return Response({"message":"Something went wrong"},status = status.HTTP_400_BAD_REQUEST)

class GetAllNotificationView(GenericAPIView):
   serializer_class = GetNotificationSerializer
   permission_classes = (IsAuthenticated,)

   def get(self,request,*args, **kwargs):
      data = []
      one_week_ago = timezone.now() - timezone.timedelta(days=7)
      Notifications = Notification.objects.filter(user = self.request.user).filter(timestamp__range=[one_week_ago,timezone.now()])
      for n in Notifications:
         serializer = GetNotificationSerializer(n)
         data.append(serializer.data)
      message_data = data[::-1]
      return Response({"message":"Here are all your notifications from the last week!","data":message_data},status = status.HTTP_200_OK)

class GetReadNotificationsView(GenericAPIView):
   serializer_class = GetNotificationSerializer
   permission_classes = (IsAuthenticated,)

   def get(self,request,*args, **kwargs):
      data = []
      one_week_ago = timezone.now() - timezone.timedelta(days=7)
      Notifications = Notification.objects.filter(user = self.request.user).filter(timestamp__range=[one_week_ago,timezone.now()]).filter(is_read = True)
      for n in Notifications:
          serializer = GetNotificationSerializer(n)
          data.append(serializer.data)
      message_data = data[::-1]
      return Response({"message":"Here are all your seen messages from the last week!","data":message_data},status = status.HTTP_200_OK)

class GetUnreadNotificationsView(GenericAPIView):
   serializer_class = GetNotificationSerializer
   permission_classes = (IsAuthenticated,)

   def get(self,request,*args, **kwargs):
      data = []
      one_week_ago = timezone.now() - timezone.timedelta(days=7)
      Notifications = Notification.objects.filter(user = self.request.user).filter(timestamp__range=[one_week_ago,timezone.now()]).filter(is_read = False)
      for n in Notifications:
          serializer = GetNotificationSerializer(n)
          data.append(serializer.data)
      message_data = data[::-1]
      return Response({"message":"Here are all your unread messages from the last week!","data":message_data},status = status.HTTP_200_OK)

class SeeNotificationView(GenericAPIView):
   serializer_class = GetNotificationSerializer
   permission_classes = (IsAuthenticated,)

   def get(self,request,*args, **kwargs):
      id = self.request.query_params.get('id')
      notif = Notification.objects.get(id = id)
      if notif.user == self.request.user:
         notif.is_read = True
         notif.save()
         notif_data = GetNotificationSerializer(notif)
         return Response({"message":"Fetched succesfully","data":notif_data.data},status = status.HTTP_200_OK)
      else:
         return Response({"message":"Not Authorized"},status = status.HTTP_400_BAD_REQUEST)