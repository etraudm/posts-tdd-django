from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker
from mixer.backend.django import mixer

from backend.models import PostComments
from backend.models.post import Post


class PostCommentsTestCase(TestCase):

    def setUp(self) -> None:
        self.faker = Faker()

    def test_comment_creation(self):
        """" ensure comment is being created """
        mock_user = mixer.blend(User)
        mock_post = mixer.blend(Post)
        post_comment = PostComments(
            post=mock_post,
            user=mock_user,
            body=self.faker.sentence()
        )
        post_comment.save()
        self.assertEqual(PostComments.objects.count(), 1)

    def test_to_string_representation(self):
        """" ensure post comment  __str__ returns a valid to string """
        mock_post_comment = mixer.blend(PostComments)
        self.assertEqual(str(mock_post_comment), '{}-{}'.format(mock_post_comment.id, mock_post_comment.body))

    def test_should_have_registered_in_admin(self):
        """" ensure comment model is registered in admin """
        self.assertTrue(admin.site.is_registered(PostComments))
