from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker
from mixer.backend.django import mixer

from backend.models.post import Post
from backend.serializers.post_serializer import PostSerializer


class PostTestCase(TestCase):

    def setUp(self) -> None:
        self.faker = Faker()

    def test_post_creation(self):
        """" ensure post is being created """
        mock_user = mixer.blend(User)
        post = Post(
            user=mock_user,
            title=self.faker.sentence(),
            body=self.faker.sentence()
        )
        post.save()
        self.assertEqual(Post.objects.count(), 1)

    def test_to_string_representation(self):
        """" ensure __str__ returns a valid to string """
        mock_post = mixer.blend(Post)
        self.assertEqual(str(mock_post), '{}-{}'.format(mock_post.post_id, mock_post.title))

    def test_should_have_registered_in_admin(self):
        """" ensure post model is registered in admin """
        self.assertTrue(admin.site.is_registered(Post))
