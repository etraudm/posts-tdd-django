from django.http import HttpResponse
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from oauth2_provider.views import ProtectedResourceView
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, \
    DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from backend.models import Post
from backend.serializers.post_serializer import PostSerializer


class PostView(GenericViewSet,  # generic view functionality
               CreateModelMixin,  # handles POSTs
               RetrieveModelMixin,  # handles GETs for 1 Company
               UpdateModelMixin,  # handles PUTs and PATCHes
               DestroyModelMixin, # delete
               ListModelMixin):  # handles GETs for many Companies

    serializer_class = PostSerializer
    permission_classes = [TokenHasReadWriteScope]
    authentication_classes = [OAuth2Authentication]
    queryset = Post.objects.all()
