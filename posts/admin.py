from django.contrib import admin
from .models import Post, Hashtag, PostImages

# Register your models here.

admin.site.register(Post)
admin.site.register(Hashtag)
admin.site.register(PostImages)