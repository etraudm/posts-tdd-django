import uuid

from django.contrib.auth.models import User
from django.db import models

from backend.models import TimestampableMixin


class Post(TimestampableMixin, models.Model):
    post_id = models.UUIDField(help_text="Post ID", default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, help_text="User", null=False, blank=False, on_delete=models.CASCADE)
    title = models.CharField("Post Title", max_length=150, null=False, blank=False)
    body = models.TextField("Body Title", null=False, blank=False)

    def __str__(self):
        return '{}-{}'.format(self.post_id, self.title)
