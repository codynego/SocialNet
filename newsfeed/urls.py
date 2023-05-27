from django.urls import path
from .views import SearchUser, SearchPost, SearchHashtag, Search

urlpatterns = [
    path('search/', Search.as_view(), name='search'),
    path('search/users/', SearchUser.as_view(), name='usersearch'),
    path('search/posts/', SearchPost.as_view(), name='postsearch'),
    path('search/hashtags/', SearchHashtag.as_view(), name='hashtagsearch'),
]