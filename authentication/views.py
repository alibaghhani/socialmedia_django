from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, RedirectView, DetailView, UpdateView
from .models import User
from social_meddia.models import *
from .forms import UserRegistrationForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from django.core.mail import EmailMessage


# Create your views here.


class SignupView(CreateView):
    model = User
    # form_class = UserRegistrationForm
    fields = ['username', 'email', 'password', 'phone_number', 'biography', 'hobbies', 'gender', 'profile']
    success_url = reverse_lazy('home')
    template_name = 'signup.html'

    # def form_valid(self, form):
    #     user = form.save(commit=False)
    #     user.is_active = False
    #     user.save()
    #     current_site = get_current_site(self.request)
    #     mail_subject = 'activate your account!.'
    #     message = render_to_string('activate_account.html', {
    #         'user': user,
    #         'domain': current_site.domain,
    #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #         'token': account_activation_token.make_token(user),
    #     })
    #     to_email = form.cleaned_data.get('email')
    #     email = EmailMessage(
    #         mail_subject, message, to=[to_email]
    #     )
    #     email.send()
    #     return HttpResponse('Please confirm your email address to complete the registration')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request,template_name='verification_message.html')
    else:
        return HttpResponse('Activation link is invalid!')

    # def send_verification_email(self, user):
    #     subject = 'Verify your email address'
    #     message = 'Please click the link below to verify your email address.'
    #     from_email = settings.EMAIL_HOST_USER
    #     to_email = user.email
    #     send_mail(subject, message, from_email, [to_email])

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)


class SigninView(LoginView):
    model = User
    next_page = reverse_lazy('home')
    template_name = 'login.html'

    # def form_valid(self, form):
    #     print('status: 200')
    #     result = super().form_valid(form)
    #     print('status: 200')
    #     # Perform additional actions after successful form validation
    #     # For example, you could log the user's login activity
    #     user = form.get_user()
    #     # Log user activity, such as login time
    #     # Example: user.log_activity('logged in')
    #     print('status: 200')
    #     # Return the result of the parent class's form_valid method
    #     return result

    # def form_valid(self, form):
    #     result = super().form_valid(form)
    #     return result


#
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         print("Username entered:", username)
#         print("Password entered:", password)
#
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             print("User authenticated successfully:", user)
#             login(request, user)
#             # Redirect to a success page or homepage
#             return redirect('home')
#         else:
#             print("Authentication failed for user:", username)
#             # Display an error message to the user
#             error_message = "Invalid username or password. Please try again."
#             return render(request, 'login.html', {'error_message': error_message})
#     else:
#         # Handle GET request for login page
#         return render(request, 'login.html')


class LogoutView(View):
    login_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('home'))


class ProfileView(DetailView, LoginRequiredMixin):
    login_url = reverse_lazy('login')
    template_name = 'profile.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        user_posts = Post.objects.filter(user=user)
        user_post_images = Image.objects.filter(post__in=user_posts,
                                                created_time__date__in=[post.created_at.date() for post in user_posts])
        context['user_posts'] = user_posts
        context['user_post_images'] = user_post_images
        follower = Follow.objects.filter(follower=self.request.user,following=user)
        if follower.exists():
            is_followed = True
        else:
            is_followed = False
        context['is_followed'] = is_followed
        return context


class ChangeInformationView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('home')
    fields = ['username', 'hobbies', 'biography', 'profile']
    template_name = 'change_username.html'
    login_url = reverse_lazy('login')


# class ChangeUsernameView(View):
#

# class ChangeBiographyView(LoginRequiredMixin, UpdateView):
#     model = User
#     success_url = reverse_lazy('home')
#     fields = ['biography']
#     template_name = 'change_bio.html'
#     login_url = reverse_lazy('login')
#
#
# class ChangeHobbiesView(LoginRequiredMixin, UpdateView):
#     model = User
#     success_url = reverse_lazy('home')
#     fields = ['hobbies']
#     template_name = 'change_hobbies.html'
#     login_url = reverse_lazy('login')


class SettingsView(DetailView, LoginRequiredMixin):
    model = User
    template_name = 'settings.html'
    context_object_name = 'user'
    login_url = reverse_lazy('login')


class UsersResetPasswordView(PasswordResetView):
    template_name = 'reset_password.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'reset_password_email.html'


class UsersPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class UsersConfirmNewPasswordView(PasswordResetConfirmView):
    template_name = 'confirm_reset_password.html'
    success_url = reverse_lazy('complete_password_change')


class UsersCompletePasswordChangeView(PasswordResetCompleteView):
    template_name = 'complete_change_password.html'
