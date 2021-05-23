import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from oauth2_provider.models import Application, AccessToken
from oauth2_provider.settings import oauth2_settings
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from rest_framework import status
from django.urls import reverse


class PostTestCase(APITestCase):

    def setUp(self) -> None:
        self.test_user = User.objects.create_user("test_user", "test@user.com", "123456")

        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost http://example.com http://example.it",
            user=self.test_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
        )
        self.application.save()

        oauth2_settings._SCOPES = ['read', 'write']

        self.token = AccessToken.objects.create(user=self.test_user, token='1234567890',
                                                application=self.application,
                                                expires=timezone.now() + datetime.timedelta(days=1),
                                                scope='read write')
        self.client = APIClient()
        print(self.token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.token))

    def tearDown(self):
        self.application.delete()
        self.test_user.delete()

    def test_should_return_ok_on_get(self):
        """ ensure view return 200 on get request """
        data = {'name': 'DabApps'}
        url = reverse('api-post-create', kwargs={'version': 'v1'})
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
