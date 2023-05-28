from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from posts.models import Post
from userprofile.models import User
from rest_framework.response import Response
from django.http import JsonResponse
from posts.serializers import PostSerializer
from .feeds_algorithm import FeedAlgorithm

# Create your views here.

class Timeline(APIView):
    def get(self, request):
        user = request.user
        feeds = FeedAlgorithm(user=user).get_feed()
        serializer = PostSerializer(feeds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
