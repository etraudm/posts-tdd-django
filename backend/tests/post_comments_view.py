import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from mixer.backend.django import mixer
from oauth2_provider.models import Application, AccessToken
from oauth2_provider.settings import oauth2_settings
from rest_framework import status
from rest_framework.test import APIClient, APITransactionTestCase, APITestCase

from backend.models import Post


class PostCommentsAPITestCase(APITestCase):

    def shortDescription(self):
        doc = self.__str__()
        return doc or None

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

    def test_restrict_route_posts(self):
        """ ensure view returns 401 if wrong token is provided """
        self.client.credentials(HTTP_AUTHORIZATION='Bearer wrong_token')
        url = reverse('api-post-comments-create', kwargs={'version': 'v1'})
        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_return_400_if_no_postid_is_provided_post(self):
        """ ensure view returns 400 if no postid is provided post """
        data = {
            'body': self.faker.paragraph(nb_sentences=3),
            'user': self.test_user.id
        }
        url = reverse('api-post-comments-create', kwargs={'version': 'v1'})
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            "errors": [
                {
                    "field": "post",
                    "message": [
                        "This field is required."
                    ]
                }
            ]
        })


