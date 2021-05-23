import uuid

from django.contrib.auth.models import User
from django.db import models

from backend.models import TimestampableMixin, Post


class PostComments(TimestampableMixin, models.Model):
    id = models.UUIDField(help_text="Post Comment ID", default=uuid.uuid4().hex, editable=False, primary_key=True)
    user = models.ForeignKey(User, help_text="User", null=False, blank=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, help_text="Post", null=False, blank=False, on_delete=models.CASCADE)
    body = models.TextField("Body", null=False, blank=False)

    def __str__(self):
        return '{}-{}'.format(self.id, self.body)
