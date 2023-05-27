from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, FollowerSerializer

# Create your views here.
class AllUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class Userme(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FollowersView(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        followers = user.followers.all()
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FollowingView(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        followers = user.following.all()
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
  
class Follow(APIView):
    def post(self, request, user_id):
        #user_id = request.data.get('id')
        if User.objects.filter(id=user_id).exists():
            follower = request.user
            user = User.objects.get(id=user_id)
            user.followers.add(follower)
        else:
            return Response("user doesnt exist", status=status.HTTP_400_BAD_REQUEST)
        return Response("you are now following this person", status=status.HTTP_201_CREATED)
    
    def delete(self, request, user_id):
        #userid = request.data.get('id')
        if User.objects.filter(id=user_id).exists():
            follower = request.user
            user = User.objects.get(id=user_id)
            follower.following.remove(user)
            user.save()
        else:
            return Response("user doesnt exist", status=status.HTTP_400_BAD_REQUEST)
        return Response("you unfollowed this user", status=status.HTTP_201_CREATED)
    
