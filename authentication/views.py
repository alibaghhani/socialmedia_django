from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, RedirectView, DetailView

from .models import User
# Create your views here.


class SignupView(CreateView):
    model = User
    fields = ['username','password','phone_number','biography','hobbies','gender']
    success_url = reverse_lazy('signup')
    template_name = 'signup.html'

class SigninView(LoginView):
    model = User
    next_page = reverse_lazy('signup')
    template_name = 'login.html'

    def form_valid(self, form):
        result = super().form_valid(form)
        return result

