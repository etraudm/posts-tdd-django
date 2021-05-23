from backend.views.post_view import PostCreateView
from django.urls import path

urlpatterns = [
    path('posts/', PostCreateView.as_view(), name='api-post-create'),
]
