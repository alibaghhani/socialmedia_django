from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
from .models import *
from .forms import *
from django.contrib import messages
from django.forms import modelformset_factory
from .forms import ImageForm,CommentCreateForm
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

class HomepageView(TemplateView):
    template_name = 'home.html'


class ExploreView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'explore.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.model
        user_posts = Post.objects.filter(user=user)
        user_post_images = Image.objects.filter(post__in=user_posts,
                                                created_time__date__in=[post.created_at.date() for post in user_posts])
        context['user_posts'] = user_posts
        context['user_post_images'] = user_post_images
        return context


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
    if request.method == 'POST':

        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Image.objects.none())

        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()

            for form in formset.cleaned_data:

                if form:
                    image = form['image']
                    photo = Image(post=post_form, image=image)
                    photo.save()

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


#


# class user_posts(DetailView):

class PostDisplayView(DetailView):
    model = User
    template_name = 'posts.html'
    context_object_name = 'user'


# class LikePostView(DetailView):
#     model = Post
#     template_name = 'profile.html'
#     context_object_name = 'post'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
#         liked = False
#         if likes_connected.like.filter(id=self.request.user.id).exists():
#             liked = True
#         context['number_of_likes'] = likes_connected.get_like_count()
#         context['post_is_liked'] = liked
#         return context



def LikePostView(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)
    return HttpResponseRedirect(reverse('profile', args=[pk]))

class UsersListView(ListView):
    model = User
    template_name = 'users_list.html'
    context_object_name = 'users'


class FollowView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        following = Follow.objects.filter(follower=request.user, following=user)
        if following.exists():
            messages.error(request,'you have already followed this user')
        else:
            following = Follow(follower=request.user, following=user)
            following.save()
            messages.success(request,'user was followed')
        return redirect('profile',user.id)

class UnfollowView(LoginRequiredMixin,View):
    login_url = reverse_lazy('login')
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        following = Follow.objects.filter(follower=request.user,following=user)
        if following.exists():
            following.delete()
            messages.success(request,'user was unfollowed!')
        else:
            messages.error(request,'you must follow this user first!')
        return redirect('profile',user.id)

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comment_post.filter(is_replied=False)
        context['post'] = post
        context['comments'] = comments

        return context

class CreateCommentView(CreateView):
    form_class =  CommentCreateForm
    template_name = 'comment.html'
    model = Comment
    success_url = reverse_lazy('home')



from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import Post, Image


class EditPostView(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'edit_post.html'
    success_url = reverse_lazy('home')


