from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView
from .models import *
from .forms import *
from django.contrib import messages
from django.forms import modelformset_factory
from .forms import ImageForm


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

# class UploadPostView(LoginRequiredMixin, CreateView):
#     model = Post
#     form_class = UploadPostForm
#     template_name = 'post_upload.html'
#     success_url = reverse_lazy('home')
#     login_url = reverse_lazy('login')
#
#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         messages.success(self.request, "Post uploaded successfully")
#         return super().form_valid(form)


class SearchUsersView(ListView):
    template_name = 'search_users.html'
    model = User

    def get_queryset(self):
        name = self.kwargs.get('name', '')
        user_list = self.model.objects.all()
        if name:
            user_list = User.objects.filter(username__contains=name)
        return user_list


# class PostView(View, LoginRequiredMixin):
#     login_url = reverse_lazy('login')
#
#     ImageFormSet = modelformset_factory(Image,
#                                         form=ImageForm, extra=3)
#
#     def post(self, request):
#         if request.method == 'POST':
#             post_form = UploadPostForm(request.POST)
#             formset = self.ImageFormSet(request.FILES,
#                                         queryset=Image.objects.none())
#             if post_form.is_valid() and formset.is_valid():
#                 post_form = post_form.save(commit=False)
#                 post_form.user = request.user
#                 post_form.save()
#                 for form in formset.cleaned_data:
#                     if form:
#                         image = form['image']
#                         photo = Image(post=post_form,
#                                       image=image)
#                         photo.save()
#                 messages.success(request,
#                                  "Yeeew, check it out on the home page!")
#                 return HttpResponseRedirect(reverse_lazy('home'))
#             else:
#                 print(post_form.errors, formset.errors)
#         else:
#             post_form = UploadPostForm()
#             formset = self.ImageFormSet(queryset=Image.objects.none())
#         return render(request,'post_upload.html',
#                       {'postForm': post_form, 'formset': formset})





@login_required
def post_upload(request):
    ImageFormSet = modelformset_factory(Image,
                                        form=ImageForm, extra=3)
    # 'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':

        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Image.objects.none())

        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()

            for form in formset.cleaned_data:
                # this helps to not crash if the user
                # do not upload all the photos
                if form:
                    image = form['image']
                    photo = Image(post=post_form, image=image)
                    photo.save()
            # use django messages framework
            messages.success(request,
                             "Yeeew, check it out on the home page!")
            return HttpResponseRedirect("/")
        else:
            print(postForm.errors, formset.errors)
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'post_upload.html',
                  {'postForm': postForm, 'formset': formset})