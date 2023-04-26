from django.contrib import admin
from blog.models import Post, Comment

from blog.models import Favorite

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Favorite)