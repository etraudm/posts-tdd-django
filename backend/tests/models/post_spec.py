import time
from unittest import mock
from unittest.mock import Mock

from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker
from mixer.backend.django import mixer

from backend.models.post import Post


class PostTestCase(TestCase):

    def setUp(self) -> None:
        self.faker = Faker()

    def test_to_string_method(self):
        """" ensure __str__ returns a valid to string """
        mock_post = mixer.blend(Post)
        self.assertEqual(str(mock_post), '{}-{}'.format(mock_post.post_id, mock_post.title))


