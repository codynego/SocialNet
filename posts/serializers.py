from rest_framework import serializers
from .models import Post, Comment, Hashtag
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
    


class PostSerializer(serializers.ModelSerializer):
    hashtags = HashtagSerializer(many=True)
    #comment = CommentSerializer(many=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id','author', 'text', 'created', 'publish', 'hashtags', 'like_count', 'comment_count']

    def create(self, validated_data):
        hashtags_data = validated_data.pop('hashtags')
        post = Post.objects.create(**validated_data)
        for hashtag_data in hashtags_data:
            hashtag_name = hashtag_data['name']
            hashtag, _ = Hashtag.objects.get_or_create(name=hashtag_name)
            post.hashtags.add(hashtag)
        return post
    
    def get_like_count(self, instance):
        return instance.likes.count()
    
    def get_comment_count(self, instance):
        return instance.comment.count()


class LikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    author_id = serializers.IntegerField()

