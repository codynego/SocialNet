from django.contrib import admin
from .models import Post, Hashtag

# Register your models here.

admin.site.register(Post)
admin.site.register(Hashtag)