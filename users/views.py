from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import SignUpForm, CustomAuthenticationForm
from items.models import Item
from .models import CustomUser

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('users:login')
    template_name = 'signup.html'

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    pass

class LikedItemsListView(ListView):
    model = Item
    template_name = 'liked_items_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs['username'])
        return user.liked_items.all()

class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = get_object_or_404(CustomUser, username=self.kwargs['username'])
        context['profile_user'] = profile_user
        context['items_for_sale'] = Item.objects.filter(author=profile_user)

        if self.request.user.is_authenticated:
            context['is_following'] = profile_user.followers.filter(id=self.request.user.id).exists()

        return context

class FollowersListView(ListView):
    model = CustomUser
    template_name = 'followers_list.html'
    context_object_name = 'followers'

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs['username'])
        return user.followers.all()

class FollowingListView(ListView):
    model = CustomUser
    template_name = 'following_list.html'
    context_object_name = 'following'

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs['username'])
        return user.following.all()

@login_required
def follow(request, username):
    user_to_follow = get_object_or_404(CustomUser, username=username)
    if request.user != user_to_follow:
        if user_to_follow.followers.filter(id=request.user.id).exists():
            user_to_follow.followers.remove(request.user)
        else:
            user_to_follow.followers.add(request.user)
    return HttpResponseRedirect(reverse('users:profile', args=[username]))
