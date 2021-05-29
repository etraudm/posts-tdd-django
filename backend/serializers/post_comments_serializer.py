from rest_framework import serializers

from backend.models import PostComments
from .user_serializer import UserSerializer


class PostCommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PostComments
        fields = '__all__'


class PostCommentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComments
        fields = '__all__'
