from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView
from posts.forms import PostForm
from posts.models import Post, Like


class LikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        is_liked = False
        if request.user.is_authenticated:
            is_liked = post.likes.filter(user=request.user).exists()
        return JsonResponse({'is_liked': is_liked})

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if not post.likes.filter(user=request.user).exists():
            Like.objects.create(user=request.user, post=post)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'post_create.html'
    model = Post
    form_class = PostForm
    success_message = 'Статья создана'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')
