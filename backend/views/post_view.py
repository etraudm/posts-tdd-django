from django.http import HttpResponse
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from oauth2_provider.views import ProtectedResourceView
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from backend.serializers.post_serializer import PostSerializer


class PostCreateView(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [TokenHasReadWriteScope]
    authentication_classes = [OAuth2Authentication]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


