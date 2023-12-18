from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from .serializers import PostSerializer
from .models import Notification,Likes

class PostPagination(PageNumberPagination):
    page_size = 10  
    page_size_query_param = 'page_size'
    max_page_size = 100
  
class FeedView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostPagination
    permission_classes = (AllowAny,)
    queryset = Notification.objects.all()
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return render(request, 'feed.html', {'results': response.data})
    

class PostCreateView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Notification.objects.all()

    def get(self, request, *args, **kwargs):
        return render(request, 'create_post.html')
    def create(self, request, *args, **kwargs):
        if self.request.query_params.get('id') is None:
           serializer = self.get_serializer(data=request.data)
           serializer.is_valid(raise_exception=True)
           self.perform_create(serializer)
           post_data = PostSerializer(serializer.instance).data
           return render(request, 'post_created.html', {'post': post_data})
        else:
            parent_id = self.request.query_params.get('id')
            parent = Notification.objects.get(id = parent_id)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            comment = serializer.instance
            comment.parent_post = parent
            comment.save()
            comment_data = PostSerializer(comment)
            return render(request,'post_created.html',{'post':comment_data.data})
         
    def perform_create(self,serializer):
        serializer.save(user = self.request.user)
        
class PostLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        post = Notification.objects.get(id = id)
        try:
          like = Likes.objects.get(post_id = post,liked_by = self.request.user)
          like.delete()
        except:
          Likes.objects.create(post_id = post,liked_by = self.request.user)
        return Response({"Message":"Succesfull"})

class GetLikesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        Post = Notification.objects.get(id = id)
        likes = Likes.objects.filter(post_id  = Post).count()
        return Response({"Likes":likes})

class GetCommentsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_comments_recursive(self, parent_post):
        comments = Notification.objects.filter(parent_post=parent_post)
        comment_data = []
        for comment in comments:
            serializer = PostSerializer(comment)
            serializer_data = serializer.data
            serializer_data["replies"] = self.get_comments_recursive(comment)
            comment_data.append(serializer_data)
        return comment_data

    def get(self, request):
        parent_id = self.request.query_params.get('id')
        parent_post = Notification.objects.get(id=parent_id)
        
        comment_data = PostSerializer(parent_post).data
        comment_data["replies"] = self.get_comments_recursive(parent_post)

        return Response({"data": comment_data}, status=status.HTTP_200_OK)

class GetCommentCount(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        post = Notification.objects.get(id = id)
        return Notification.objects.filter(parent_post = post).count()