from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, RedirectView, DetailView
from .models import User
from social_meddia.models import *
# Create your views here.


class SignupView(CreateView):
    model = User
    fields = ['username','password','phone_number','biography','hobbies','gender']
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        
        return response

class SigninView(LoginView):
    model = User
    next_page = reverse_lazy('home')
    template_name = 'login.html'

    def form_valid(self, form):
        result = super().form_valid(form)
        return result

class LogoutView(View,LoginRequiredMixin):
    login_url = reverse_lazy('home')
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('home'))

class ProfileView(DetailView,LoginRequiredMixin):
    login_url = reverse_lazy('login')
    template_name = 'profile.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['user_posts'] = Post.objects.filter(user=user)
        return context
