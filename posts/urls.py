from django.urls import path
from .views import PostView, HashtagView, CommentView, LikeView, Hashtagdetail, Postdetails, UserPosts, Commentdelete, HashtagList

urlpatterns = [
    # post endpoint
    path('posts/', PostView.as_view(), name='posts'),
    path('posts/<int:pk>/', Postdetails.as_view(), name='post'),
    path('users/<int:pk>/posts/', UserPosts.as_view(), name='userposts'),
    path('posts/<int:pk>/comments/', CommentView.as_view(), name='comment'),
    path('posts/<int:post_id>/comments/<int:pk>/', Commentdelete.as_view(), name='comment_delete'),
    path('posts/<int:post_id>/like/', LikeView.as_view(), name='like'),
    path('hashtags/', HashtagView.as_view(), name='hashtags'),
    path('hashtags/trending/', HashtagView.as_view(), name='hashtags'),
    path('hashtags/<int:pk>/', Hashtagdetail.as_view(), name='hashtag'),
]