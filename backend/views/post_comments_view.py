from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, \
    DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from backend.models import PostComments
from backend.serializers import PostCommentsSerializer, PostCommentsCreateSerializer


class PostCommentsView(GenericViewSet,  # generic view functionality
                       CreateModelMixin,  # handles POSTs
                       ListModelMixin):  # handles GETs for many Companies
    """

    Returns a list of all post in the system.
    """

    permission_classes = [TokenHasReadWriteScope]
    authentication_classes = [OAuth2Authentication]
    queryset = PostComments.objects.all()
    serializer_class = PostCommentsSerializer

    action_serializers = {
        'list_from_post': PostCommentsSerializer,
        'create': PostCommentsCreateSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(PostCommentsView, self).get_serializer_class()

    @swagger_auto_schema(tags=["Post Comments"])
    def create(self, request, *args, **kwargs):
        """
        Create a comment

        Method to create a comment
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Post Comments"])
    def list_from_post(self, request, *args, **kwargs):
        """
        List all comments of a post

        Method to list comments of a post
        """
        queryset = PostComments.objects.filter(post__post_id=str(self.kwargs['pk']))
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
