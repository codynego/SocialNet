from django.shortcuts import render
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from posts.models import Post, Comment

# Create your views here.

@receiver(post_save, sender=Post)
def post_notifications(sender, instance, created, **kwargs):
    if created:
        followers = instance.author.followers.all()
        for follower in followers:
            message = f'New post by {instance.author.username}'
            Notification.objects.create(recipient=follower, sender=instance.author, message=message)


@receiver(post_save, sender=Comment)
def comment_notifications(instance, sender, created, **kwargs):
    if created:
        recipient = instance.post.author
        if recipient != instance.author:
            message = f"{instance.author} commented on your post"
            Notification.objects.create(recipient=recipient,
                                        sender=instance.author,
                                        message=message)
