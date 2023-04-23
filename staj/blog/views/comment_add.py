from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from posts.forms import CommentForm
from posts.models import Post, Comment


class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'comment_create.html'
    form_class = CommentForm

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        text = form.cleaned_data['text']
        post = get_object_or_404(Post, pk=post_pk)
        form.instance.author = self.request.user
        form.instance.post = post
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        post_pk = self.kwargs['pk']
        return reverse_lazy('post_detail', kwargs={'pk': post_pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['post_pk'] = self.kwargs['pk']
        return kwargs
