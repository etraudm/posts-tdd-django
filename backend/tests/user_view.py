import datetime
import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from mixer.backend.django import mixer
from oauth2_provider.models import Application, AccessToken
from oauth2_provider.settings import oauth2_settings
from rest_framework import status
from rest_framework.test import APITransactionTestCase, APIClient

from backend.tests import bcolors


class UserAPITestCase(APITransactionTestCase):

    def setUp(self) -> None:
        self.faker = Faker()
        self.test_user = mixer.blend(User)
        self.application = mixer.blend(Application,
                                       user=self.test_user,
                                       client_type=Application.CLIENT_CONFIDENTIAL,
                                       authorization_grant_type=Application.GRANT_PASSWORD,
                                       )

        oauth2_settings._SCOPES = ['read', 'write']
        self.token = mixer.blend(AccessToken, user=self.test_user,
                                 application=self.application,
                                 expires=timezone.now() + datetime.timedelta(days=1),
                                 scope='read write')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.token))

    def tearDown(self):
        self.application.delete()
        self.test_user.delete()

    def test_should_return_401_if_wrong_token_is_provided(self):
        """ should return 401 if wrong token is provided """
        self.client.credentials(HTTP_AUTHORIZATION='wrong token')
        url = reverse('api-user-update-get', kwargs={'version': 'v1'})
        response: HttpResponse = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_user_data(self):
        """ should return the logged user """

        url = reverse('api-user-update-get', kwargs={'version': 'v1'})
        response: HttpResponse = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['id'], self.test_user.id)
