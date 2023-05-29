from rest_framework import serializers
from .models import Post, Comment, Hashtag, PostImages
from userprofile.models import User
from userprofile.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','author', 'text', 'post', 'created']
        read_only_fields = ('author', 'post', 'created')

    def create(self, validated_data):
        post = self.context['post']  # Retrieve the post from the context

        user = self.context['request']
        comment = Comment.objects.create(post=post, author=user, **validated_data)
        return comment


class HashtagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = ('id', 'name')



class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('id', 'name')

    def to_representation(self, instance):
        return instance.name
    
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = ['id', 'image']

class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    #hashtags = HashtagSerializer(many=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    upload_images = serializers.ListField(
        child = serializers.ImageField(max_length=1000000,
                                       allow_empty_file=False,
                                       use_url=False),
        write_only=True
    )

    class Meta:
        model = Post
        fields = ['id','author', 'text', 'created', 'publish', 'like_count', 'comment_count', 'images', 'upload_images']

    def create(self, validated_data):
        #hashtags_data = validated_data.pop('hashtags')
        images = validated_data.pop('upload_images')
        post = Post.objects.create(**validated_data)
        for image in images:
            PostImages.objects.create(post=post, image=image) 
        """for hashtag_data in hashtags_data:
            hashtag_name = hashtag_data['name']
            hashtag, _ = Hashtag.objects.get_or_create(name=hashtag_name)
            post.hashtags.add(hashtag)"""
        return post
    
    def get_like_count(self, instance):
        return instance.likes.count()
    
    def get_comment_count(self, instance):
        return instance.comment.count()


class LikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    author_id = serializers.IntegerField()

