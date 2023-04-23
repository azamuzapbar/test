from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView



from posts.forms import SearchForm

from posts.models import Post

from accounts.forms import CustomUserCreationForm, UserChangeForm,LoginForm

from accounts.models import Account


def subscribe_to_account(request, pk):
    account_to_subscribe = get_object_or_404(Account, pk=pk)

    if request.user == account_to_subscribe:
        messages.error(request, 'Вы не можете подписаться на себя.')
        return redirect('index')

    if account_to_subscribe.subscribers.filter(pk=request.user.pk).exists():
        messages.info(request, 'Вы уже подписаны на этот аккаунт.')
        return redirect('index')

    request.user.subscriptions.add(account_to_subscribe)
    account_to_subscribe.subscribers_count += 1
    account_to_subscribe.save()
    request.user.save()
    messages.success(request, f'Вы успешно подписались на {account_to_subscribe.username}.')
    return redirect('index')


class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            messages.error(request, "Некорректные данные")
            return redirect('login')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email= email, password=password)
        if not user:
            messages.warning(request, "Пользователь не найден")
            return redirect('login')
        login(request, user)
        messages.success(request, 'Добро пожаловать')
        next = request.GET.get('next')
        if next:
            return redirect(next)
        return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('login')


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(self.success_url)
        context = {'form': form}
        return self.render_to_response(context)


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SearchForm
        user = self.get_object()
        context['form'] = form
        context['posts'] = Post.objects.filter(author=user).order_by('-created_at')
        return context


class UserChangeView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return UserChangeForm(**form_kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()

        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

    def subscribe(self, user):
        """
        Add a subscription to another user
        """
        if self.subscriptions.filter(pk=user.pk).exists():
            return False  # Subscription already exists
        else:
            self.subscriptions.add(user)
            self.subscriptions_count += 1
            self.save()
            user.subscribers_count += 1
            user.save()
            return True

    def unsubscribe(self, user):
        """
        Remove a subscription from another user
        """
        if self.subscriptions.filter(pk=user.pk).exists():
            self.subscriptions.remove(user)
            self.subscriptions_count -= 1
            self.save()
            user.subscribers_count -= 1
            user.save()
            return True
        else:
            return False

