from userprofile.models import User
from posts.models import Post
from .feeds_algorithm import FeedAlgorithm

user = User.objects.get(id=1)
feeds = FeedAlgorithm(user=user)

print(feeds)
