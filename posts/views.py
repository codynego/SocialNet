from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from .models import Post, Hashtag, Comment
from rest_framework.response import Response
from .serializers import PostSerializer, HashtagsSerializer, CommentSerializer, LikeSerializer
from django.db import models
from userprofile.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
#####
#
##


class PostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
class Postdetails(generics.RetrieveUpdateDestroyAPIView):
    """
    retrieve, update and delete a specific post

    permission:
        superuser: only super user can perform this request
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser]


class UserPosts(APIView):
    def get(self, request, pk):
        if User.objects.filter(id=pk).exists():
            post = Post.objects.filter(author = User.objects.get(id=pk))
        else:
            return Response('User doesnt exist', status=status.HTTP_400_BAD_REQUEST)
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CommentView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if Post.objects.filter(id=pk).exists():
            comment = Comment.objects.filter(post__id=pk)
        else:
            return Response("Post doesnt exists", status=status.HTTP_400_BAD_REQUEST)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        if Post.objects.filter(id=pk).exists():
            post = Post.objects.get(id=pk)  # Retrieve the specific post
        else:
            return Response("post doesnt exist", status=status.HTTP_400_BAD_REQUEST)
        
        serializer = CommentSerializer(data=request.data, context={'post': post, 'request': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class Commentdelete(APIView):
    def delete(self, request, post_id, pk):
        if Post.objects.filter(id=post_id).exists():
            comments = Comment.objects.filter(post__id=post_id)
        else:
            return Response("Post doesnt exists", status=status.HTTP_400_BAD_REQUEST)
        comment = get_object_or_404(Comment, id=pk)
        comment.delete()
        return Response("comment deleted", status=status.HTTP_204_NO_CONTENT)

"""class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer"""


class HashtagView(generics.ListCreateAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagsSerializer

class Hashtagdetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagsSerializer

"""class HashtagList(APIView):
    def get(self, request):
        hashtags = Post.objects.values('hashtag').annotate(count=models.Count('hashtag')).order_by('-count')
        hashtag_list = [{'hashtag': hashtag['hashtag'], 'count': hashtag['count']} for hashtag in hashtags]
        return Response(hashtag_list)"""

class HashtagList(APIView):
    def get(self, request):
        hashtags = Hashtag.objects.annotate(count=models.Count('post__id')).values('name', 'count').order_by('-count')
        hashtag_list = [{'hashtag': hashtag['name'], 'count': hashtag['count']} for hashtag in hashtags]
        return Response(hashtag_list)

class LikeView(APIView):
    def post(self, request, post_id):
        author = request.user

        if Post.objects.filter(id=post_id).exists():
            post = Post.objects.get(id=post_id)
        else:
            return Response({"message": "Post not found"}, status=status.HTTP_400_BAD_REQUEST)
        post.like_post(author)
        post.save()
        return Response({"message": "post liked"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        author = request.user

        if Post.objects.filter(id=post_id).exists():
            post = Post.objects.get(id=post_id)
        else:
            return Response({"message": "Post not found"}, status=status.HTTP_400_BAD_REQUEST)
        post.unlike_post(author)
        post.save()
        return Response({"message": "post unliked"}, status=status.HTTP_400_BAD_REQUEST)