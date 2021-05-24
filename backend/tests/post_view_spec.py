import datetime
import uuid

from django.contrib.auth.models import User
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from mixer.backend.django import mixer
from oauth2_provider.models import Application, AccessToken
from oauth2_provider.settings import oauth2_settings
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APITransactionTestCase

from backend.models import Post

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PostAPITestCase(APITestCase):

    def setUp(self) -> None:
        print(bcolors.OKGREEN + self._testMethodDoc + bcolors.ENDC)
        self.faker = Faker()
        self.test_user = mixer.blend(User)
        self.application = mixer.blend(Application,
                                       user=self.test_user,
                                       client_type=Application.CLIENT_CONFIDENTIAL,
                                       authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
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

    def test_should_return_400_if_no_title_is_provided_post(self):
        """ ensure view returns 400 if no name is provided post"""
        data = {
            'body': self.faker.paragraph(nb_sentences=3),
            'user': self.test_user.id
        }
        url = reverse('api-post-create-list', kwargs={'version': 'v1'})
        response = self.client.post(url, data, format='json')

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

    def test_should_return_400_if_no_title_is_provided_put(self):
        """ ensure view returns 400 if no name is provided put"""
        data = {
            'body': self.faker.paragraph(nb_sentences=3),
            'user': self.test_user.id
        }
        post = mixer.blend(Post)

        url = reverse('api-post-update-get-delete', kwargs={'version': 'v1', 'pk': str(post.post_id)})
        response = self.client.put(url, data, format='json')

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

    def test_should_return_400_if_no_body_is_provided_post(self):
        """ ensure view returns 400 if no body is provided post """
        data = {
            'title': self.faker.text(max_nb_chars=150),
            'user': self.test_user.id
        }
        url = reverse('api-post-create-list', kwargs={'version': 'v1'})
        response = self.client.post(url, data, format='json')

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

    def test_should_return_400_if_no_body_is_provided_put(self):
        """ ensure view returns 400 if no body is provided put """
        data = {
            'title': self.faker.text(max_nb_chars=150),
            'user': self.test_user.id
        }

        post = mixer.blend(Post)

        url = reverse('api-post-update-get-delete', kwargs={'version': 'v1', 'pk': str(post.post_id)})
        response = self.client.put(url, data, format='json')

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

    def test_should_return_201_if_success(self):
        """ ensure view returns 201 if success"""
        data = {
            'title': self.faker.text(max_nb_chars=150),
            'body': self.faker.paragraph(nb_sentences=3),
            'user': str(self.test_user.id)
        }

        url = reverse('api-post-create-list', kwargs={'version': 'v1'})
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_return_200_if_success_put(self):
        """ ensure view returns 200 if success update post """
        data = {
            'title': self.faker.text(max_nb_chars=150),
            'body': self.faker.paragraph(nb_sentences=3),
            'user': self.test_user.id
        }

        post = mixer.blend(Post)

        url = reverse('api-post-update-get-delete', kwargs={'version': 'v1', 'pk': str(post.post_id)})
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_return_204_if_delete_success(self):
        """ ensure view returns 204 if delete POST success """

        post = mixer.blend(Post)

        url = reverse('api-post-update-get-delete', kwargs={'version': 'v1', 'pk': str(post.post_id)})
        response = self.client.delete(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_list_posts(self):
        """" ensure view returns a list of posts """
        posts = mixer.cycle(5).blend(Post)
        url = reverse('api-post-create-list', kwargs={'version': 'v1'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            set(post['post_id'] for post in response.data),
            set(post.post_id.__str__() for post in posts)
        )

