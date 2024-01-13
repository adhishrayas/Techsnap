from django.shortcuts import render
from rest_framework.generics import ListAPIView,CreateAPIView,GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from auth_modules.models import CustomUser
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
    queryset = Notification.objects.filter(parent_post__isnull = True)
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response
    
class MovieFeedView(APIView):
    permission_classes = (AllowAny,)
    pagination_class = PostPagination
    def get(self,request,*args, **kwargs):
        content_id = self.request.query_params.get('content_id')
        content_type = self.request.query_params.get('content_type')
        query = Notification.objects.filter(content_id = content_id,content_type = content_type)
        data = []
        for q in query:
            serializer = PostSerializer(q)
            data.append(serializer.data)
        
        #return Response({"data":data})
        return render(request,'post_feed.html',{'results':data})

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
           post = serializer.instance
           if self.request.query_params.get('content_id') is None:
              post_data = PostSerializer(post).data
              #return Response({'post':post_data})
              return render(request, 'post_created.html', {'post': post_data})
           else:
               content_id = self.request.query_params.get('content_id')
               content_type = self.request.query_params.get('content_type')
               post.content_id = content_id
               post.content_type = content_type
               post.save()
               post_data = PostSerializer(post).data
               #return Response({'post':post_data})
               return render(request,'post_created.html',{'post':post_data})
        else:
            parent_id = self.request.query_params.get('id')
            parent = Notification.objects.get(id = parent_id)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            comment = serializer.instance
            comment.parent_post = parent
            if parent.content_id == 0:
                comment.save()
                comment_data = PostSerializer(comment)
                #return Response({'post':comment_data.data})
                return render(request,'post_created.html',{'post':comment_data.data})
            else:
                comment.content_id = parent.content_id
                comment.content_type = parent.content_type
                comment.save()
                comment_data = PostSerializer(comment)
                #return Response({'post':comment_data.data})
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

    def get_comments(self, parent_post):
        comments = Notification.objects.filter(parent_post=parent_post)
        comment_data = []
        for comment in comments:
            serializer = PostSerializer(comment)
            serializer_data = serializer.data
            serializer_data["replies"] = self.get_comments(comment)
            comment_data.append(serializer_data)
        return comment_data

    def get(self, request):
        parent_id = self.request.query_params.get('id')
        parent_post = Notification.objects.get(id=parent_id)
        comment_data = {}
        comment_data["replies"] = self.get_comments(parent_post)
        return Response({"data":comment_data})
        return render(request,'post_detail.html',{"data": comment_data})

class GetCommentCount(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        post = Notification.objects.get(id = id)
        return Notification.objects.filter(parent_post = post).count()
    
class PostDetailView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get(self,request,*args, **kwargs):
        id = self.request.query_params.get('id')
        post = Notification.objects.get(id = id)
        serializer = PostSerializer(post)
        return render(request,'post_detail.html',{"data":serializer.data})
    
class UnseenLikesView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,*args, **kwargs):
        user = self.request.user
        posts = Notification.objects.filter(user = user)
        for p in posts:
           # try:
            likes = Likes.objects.filter(post_id = p).exclude(liked_by = user)
            data = []
            for l in likes:
                    obj = {}
                    by = l.liked_by
                    obj['liked_by'] = by.username
                    obj['liked_at'] = l.liked_at
                    obj['liked_on'] = l.post_id.id
                    obj['liked_by_id'] = by.id
                    data.append(obj)
            return render(request,'notifications.html',{"data":data})
           # except:
            #    return Response({"data":None})
                
class CommentsNotifsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,*args, **kwargs):
        user = self.request.user
        posts = Notification.objects.filter(user = user)
        data = []
        for p in posts:
            replies = Notification.objects.filter(parent_post = p)
            for r in replies:
                obj = {}
                obj['replied_by'] = r.user.username
                obj['replier_id'] = r.user.id
                obj['replied_on'] = p.id
                obj['replied_at'] = r.timestamp
                data.append(obj)
        return render(request,'comment_notifs.html',{"data":data})