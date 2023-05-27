from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from userprofile.models import User
from posts.models import Post, Hashtag
from userprofile.serializers import UserSerializer
from django.db.models import Q
from posts.serializers import PostSerializer, HashtagsSerializer
from django.http import JsonResponse

# Create your views here.



class Search(APIView):
    def get(self, request):
        query = request.query_params.get('q')
        user = User.objects.filter(Q(username__icontains=query))
        posts = Post.objects.filter(Q(text__icontains=query))
        hashtags = Hashtag.objects.filter(Q(name__icontains=query))
        serializer_user = UserSerializer(user, many=True).data
        serializer_post = PostSerializer(posts, many=True).data
        serializer_hashtag = HashtagsSerializer(hashtags, many=True).data

        serializer = {"user": serializer_user, "hashtags": serializer_hashtag, "posts": serializer_post}

        return Response(serializer, status=status.HTTP_200_OK)
    

class SearchUser(APIView):
    def get(self, request):
        query = request.query_params.get('q')
        user = User.objects.filter(Q(username__icontains=query))
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SearchPost(APIView):
    def get(self, request):
        query = request.query_params.get('q')
        posts = Post.objects.filter(Q(text__icontains=query))
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SearchHashtag(APIView):
    def get(self, request):
        query = request.query_params.get('q')
        hashtags = Hashtag.objects.filter(Q(name__icontains=query))
        serializer = HashtagsSerializer(hashtags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
