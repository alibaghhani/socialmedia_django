from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView
from .models import *
from .forms import UploadPostForm
from django.contrib import messages

# Create your views here.

class HomepageView(TemplateView):
    template_name = 'home.html'


class ExploreView(TemplateView):
    template_name = 'explore.html'


# class UploadPostView(LoginRequiredMixin, View):
#     login_url = reverse_lazy('login')
#     def post(self, request):
#         if request.method == 'POST':
#             form = UploadPostForm(request.POST, request.FILES)
#             if form.is_valid():
#                 cd = form.cleaned_data
#                 Post.objects.create(
#                     title=cd['title'],
#                     content=cd['content'],
#                     image=cd['image'],
#                     user=request.user
#                 )
#                 messages.success(request, "Post uploaded successfully")
#                 return redirect("home")
#
#
#         else:
#             post = UploadPostForm()
#         return render(request, "post_upload.html", {'post': post})
#
#

class UploadPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = UploadPostForm
    template_name = 'post_upload.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Post uploaded successfully")
        return super().form_valid(form)
