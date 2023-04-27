from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from blog.views.base import IndexView

from blog.views.post_add import PostCreateView

from blog.views.post_detail import PostDetailView

from blog.views.comment_add import CommentCreateView

from blog.views import post_add

from blog.views.post_add import PostDeleteView

from blog.views.base import FavoriteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
                  path('filter/likes_count/', IndexView.as_view(), name='filter_likes_count'),
                  path('filter/views_count/', IndexView.as_view(), name='filter_views_count'),
                  path('filter/created_at/', IndexView.as_view(), name='filter_created_at'),

                  path('posts/add/', PostCreateView.as_view(), name='post_add'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('posts/<int:post_id>/like/', post_add.LikeView.as_view(), name='like_post'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:pk>/confirm-delete/', PostDeleteView.as_view(), name='confirm_delete'),
    path('posts/<int:pk>/to-favorite', FavoriteView.as_view(), name='to_favorite'),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)