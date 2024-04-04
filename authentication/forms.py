from django.core.validators import RegexValidator
from django import forms
from social_meddia.models import UserProfilePicture
from .models import User
#
#
# class UserRegistrationForm(forms.ModelForm):
#     GENDER_CHOICE = (
#         ('he', 'male'),
#         ('she', 'female')
#     )
#
#     HOBBIES = (
#         ('sport', '🏆'),
#         ('music', '♫'),
#         ('movie', '🎬'),
#         ('sleeping', 'ᶻ 𝗓 𐰁'),
#         ('photography', '📷')
#     )
#     username = forms.CharField(max_length=25)
#     password = forms.CharField(max_length=250, validators=[RegexValidator(
#         regex=r"^(?=.*[A-Z])(?=.*\d).{8,}$",
#         message="Password must be at least 8 characters long and contain at least one uppercase letter and one digit."
#     )])
#     phone_number = forms.CharField(max_length=11, validators=[RegexValidator(
#         regex=r"^09[0|1|2|3][0-9]{8}$"
#     )])
#     biography = forms.CharField(max_length=20)
#     hobbies = forms.ChoiceField(choices=HOBBIES)
#     gender = forms.ChoiceField(choices=GENDER_CHOICE)
#     profile_picture = forms.ImageField()
#
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'phone_number', 'biography', 'hobbies', 'gender', 'profile_picture']
#
#     def save(self, commit=True):
#         # Save User fields
#         user_instance = super().save(commit=False)
#         user_instance.set_password(self.cleaned_data['password'])
#         user_instance.save()
#         profile_picture_instance = UserProfilePicture.objects.filter(user=user_instance).first()
#         if profile_picture_instance:
#             profile_picture_instance.profile_picture = self.cleaned_data['profile_picture']
#             profile_picture_instance.save()
#         else:
#             profile_picture_instance = UserProfilePicture.objects.create(
#                 user=user_instance,
#                 profile_picture=self.cleaned_data['profile_picture']
#             )
#
#         return user_instance
#
#

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # Assuming your User model is in the same directory

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'biography', 'hobbies', 'gender', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
