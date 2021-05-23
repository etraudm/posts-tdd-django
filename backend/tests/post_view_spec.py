import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from oauth2_provider.models import Application, AccessToken
from oauth2_provider.settings import oauth2_settings
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class PostAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.faker = Faker()
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
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(self.token))
        self.url = reverse('api-post-create', kwargs={'version': 'v1'})

    def tearDown(self):
        self.application.delete()
        self.test_user.delete()

    def test_should_return_400_if_no_title_is_provided(self):
        """ ensure view returns 400 if no name is provided """
        data = {
            'body': self.faker.paragraph(nb_sentences=3),
            'user': self.test_user.id
        }
        url = reverse('api-post-create', kwargs={'version': 'v1'})
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            "errors": [
                {
                    "field": "title",
                    "message": [
                        "This field is required."
                    ]
                }
            ]
        })

    def test_should_return_400_if_no_body_is_provided(self):
        """ ensure view returns 400 if no body is provided """
        data = {
            'title': self.faker.text(max_nb_chars=150),
            'user': self.test_user.id
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            "errors": [
                {
                    "field": "body",
                    "message": [
                        "This field is required."
                    ]
                }
            ]
        })