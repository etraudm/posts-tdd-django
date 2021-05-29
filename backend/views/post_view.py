from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from backend.models import Post
from backend.serializers.post_serializer import PostSerializer, PostSerializerCreate


class PostView(GenericViewSet,  # generic view functionality
               CreateModelMixin,  # handles POSTs
               RetrieveModelMixin,  # handles GETs for 1 Company
               UpdateModelMixin,  # handles PUTs and PATCHes
               DestroyModelMixin,  # delete
               ListModelMixin):  # handles GETs for many Companies
    """

    Returns a list of all post in the system.
    """
    serializer_class = PostSerializer

    action_serializers = {
        'list': PostSerializer,  # get request serializer
        'create': PostSerializerCreate,  # post request serializer
        'update': PostSerializerCreate
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

    permission_classes = [TokenHasReadWriteScope]
    authentication_classes = [OAuth2Authentication]
    queryset = Post.objects.all()

    @swagger_auto_schema(tags=["Posts"])
    def create(self, request, *args, **kwargs):
        """
        Create a post

        Method to create a post
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Posts"])
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a post

        Method to get details of a post
        """
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Posts"])
    def update(self, request, *args, **kwargs):
        """
        Update a post

        Method to update data of a post
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Posts"])
    def destroy(self, request, *args, **kwargs):
        """
        Delete a post

        Method to delete a post
        """
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Posts"])
    def list(self, request, *args, **kwargs):
        """
        List all posts

        Method to list posts
        """
        return super().list(request, *args, **kwargs)
