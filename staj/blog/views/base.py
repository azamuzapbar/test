from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils.http import urlencode
from django.views.generic import ListView, FormView
from blog.forms import SearchForm,FavoriteForm
from blog.models import Post, Favorite
from django.contrib import messages


class IndexView(ListView):
    template_name = 'index.html'
    model = Post
    context_object_name = 'posts'
    ordering = ['-views_count']

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by')

        if order_by == 'likes_count':
            queryset = queryset.order_by('-like_count')
        elif order_by == 'views_count':
            queryset = queryset.order_by('-views_count')
        elif order_by == 'created_at':
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        context['favorite_form'] = FavoriteForm()
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context



class FavoriteView(LoginRequiredMixin, FormView):
    form_class = FavoriteForm
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get('pk'))
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            note = form.cleaned_data.get('note')
            user = request.user
            if not Favorite.objects.filter(user=user, post=post).exists():
                Favorite.objects.create(user=user, post=post, note=note)
                messages.success(request, 'Статья была добавлена в избранное')
        return redirect('index')


