from django.shortcuts import render,redirect
from django.template.response import TemplateResponse
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView,GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .serializers import PostSerializer
from .models import Notification,Likes

class PostPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100
    def get_paginated_data(self, serializer_class, data):
        page_number = self.page.number
        total_pages = self.page.paginator.num_pages

        serialized_data = serializer_class(data['results'], many=True).data

        paginated_data = {
            'count': data['count'],
            'next': data['next'],
            'previous': data['previous'],
            'results': serialized_data,
            'page_number': page_number,
            'total_pages': total_pages,
        }

        return paginated_data
    
class FeedView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostPagination
    permission_classes = (IsAuthenticated,)
    queryset = Notification.objects.all()
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return render(request, 'feed.html', {'results': response.data})
        
'''
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        template_name = 'feed.html'
        paginator = self.paginator
        serializer_class = self.serializer_class
        paginated_data = paginator.get_paginated_data(serializer_class, response.data)
        response.data['paginated_data'] = paginated_data
        return render(request, template_name, response.data)
'''
class PostCreateView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Notification.objects.all()

    def get(self, request, *args, **kwargs):
        return render(request, 'create_post.html')
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Assuming you have a template named 'post_created.html'
        post_data = PostSerializer(serializer.instance).data
        return render(request, 'post_created.html', {'post': post_data})
    def perform_create(self,serializer):
        post = serializer.save(user = self.request.user)
        
class PostLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        post = Notification.objects.get(id = id)
        try:
          like = Likes.objects.get(post_id = post,liked_by = self.request.user)
          like.delete()
        #  return Response({"message":"Unliked"},status = status.HTTP_200_OK)
        except:
            Likes.objects.create(post_id = post,liked_by = self.request.user)
         #   return Response({"message":"Liked"},status = status.HTTP_200_OK)
        return redirect('Feed')