from backend.views.post_comments_view import PostCommentsView
from backend.views.post_view import PostView
from django.urls import path

from backend.views.user_view import UserView

urlpatterns = [
    path('user/', UserView.as_view({'get': 'get_user'}), name="api-user-update-get"),
    path('posts/comments/', PostCommentsView.as_view({'post': 'create'}), name="api-post-comments-create"),
    path('posts/<str:pk>/comments/', PostCommentsView.as_view({'get': 'list_from_post'}), name="api-post-comments-list"),
    path('posts/', PostView.as_view({'get': 'list', 'post': 'create'}), name='api-post-create-list'),
    path('posts/<str:pk>/', PostView.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'}),
         name='api-post-update-get-delete'),
]
