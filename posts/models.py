from django.db import models
from userprofile.models import User

# Create your models here.

class Hashtag(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.CharField(max_length=255)
    hashtags = models.ManyToManyField(Hashtag, symmetrical=False, related_name='post', blank=True)
    #likes = models.ManyToManyField(User, through='Like', related_name='liked_posts'),
    created = models.DateField(auto_now_add=True)
    publish = models.DateField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def like_post(self, user):
        """
        Helper method to add a user to the likes of the post.
        """
        self.likes.add(user)

    def unlike_post(self, user):
        """
        Helper method to remove a user from the likes of the post.
        """
        self.likes.remove(user)

class PostImages(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='img', default='', null=True, blank=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    created = models.DateField(auto_now_add=True)


"""class Like(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('wow', 'Wow'),
        ('haha', 'Haha'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


"""