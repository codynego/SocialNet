from django.urls import path
from .views import AllUserView, UserDetail, FollowersView, FollowingView, Follow, Userme


urlpatterns = [
    path('users/me/', Userme.as_view(), name='userme'),
    path('users/', AllUserView.as_view(), name='users'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user'),

    path('users/<int:user_id>/following/', FollowingView.as_view(), name='followings'),
    path('users/<int:user_id>/followers/', FollowersView.as_view(), name='followers'),
    path('users/<int:user_id>/follow', Follow.as_view(), name='follow'),
]