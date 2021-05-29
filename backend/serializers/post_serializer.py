from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from backend.models import Post
from .post_comments_serializer import PostCommentsSerializer
from .user_serializer import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = ['post_id', 'title', 'body', 'created_at', 'updated_at', 'user']


class PostSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
