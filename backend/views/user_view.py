from django.contrib.auth.models import User
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.renderers import JSONRenderer
from rest_framework.viewsets import GenericViewSet

from backend.serializers import UserSerializer


class UserView(GenericViewSet,  # generic view functionality
               CreateModelMixin,  # handles POSTs
               RetrieveModelMixin):
    serializer_class = UserSerializer

    permission_classes = [TokenHasReadWriteScope]
    authentication_classes = [OAuth2Authentication]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(UserView, self).get_serializer_class()

    @swagger_auto_schema(tags=["User"])
    def get_user(self, request, *args, **kwargs):
        """
        Retrieve user data

        Method to get details from logged user
        """
        user = request.user
        return HttpResponse(JSONRenderer().render(UserSerializer(user).data), content_type='application/json')
