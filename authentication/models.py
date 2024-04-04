from django.db import models

# Create your models here.
from django.db import models
# Create your models here.
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
#from social_meddia.models import UserProfilePicture
from .manager import UserManager



class User(AbstractUser):
    # def get_profile_filename(self, filename):
    #     user = self.username
    #     slug = slugify(user)
    #     return "user_profiles/%s-%s" % (slug, filename)




    GENDER_CHOICE = (
        ('he', 'male'),
        ('she', 'female')
    )

    HOBBIES = (
        ('sport', '🏆'),
        ('music', '♫'),
        ('movie', '🎬'),
        ('sleeping', 'ᶻ 𝗓 𐰁'),
        ('photography', '📷')
    )
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=250, validators=[RegexValidator(
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$",
        message="Password must be at least 8 characters long and contain at least one uppercase letter and one digit."
    )])
    phone_number = models.CharField(max_length=11, null=True, validators=[RegexValidator(
        regex=r"^09[0|1|2|3][0-9]{8}$"
    )])
    biography = models.CharField(max_length=20, default=None, null=True, blank=True)
    hobbies = models.CharField(choices=HOBBIES, max_length=250, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=250, null=True)
    email = models.EmailField(validators=[
        RegexValidator(
            regex=r"^([\w]*[\w\.]*(?!\.)@gmail.com)",
            message="enter a valid email address"

        )
    ])
    # is_admin = models.BooleanField(
    #     "superuser status",
    #     default=False,
    #     help_text="Designates whether the user is superuser.",
    # )
    profile = models.ImageField(upload_to='media',null=True,blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=False)

    # is_logged_in = models.BooleanField(default=False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','password']
    objects = UserManager()

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)

    # @property
    # def is_staff(self):
    #     if self.is_superuser == False:
    #         return False

    @property
    def profile_picture(self):
        profile_picture = self.user_profile.url
        try:
            return profile_picture
        except AttributeError:
            return None

    def get_follower_count(self):
        return self.follower.count()

    def get_following_count(self):
        return self.following.count()

    def get_posts_count(self):
        return self.posts.count()


    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
#
# from django.db import models
# from django.core.validators import RegexValidator
# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from .manager import UserManager
#
#
#
#
# class User(AbstractUser):
#     GENDER_CHOICES = (
#         ('he', 'Male'),
#         ('she', 'Female')
#     )
#
#     HOBBY_CHOICES = (
#         ('sport', '🏆'),
#         ('music', '♫'),
#         ('movie', '🎬'),
#         ('sleeping', 'ᶻ 𝗓 𐰁'),
#         ('photography', '📷')
#     )
#
#     username = models.CharField(('Username'), max_length=25, unique=True)
#     phone_number = models.CharField(('Phone Number'), max_length=11, null=True, validators=[
#         RegexValidator(regex=r'^09[0|1|2|3][0-9]{8}$', message=('Phone number must be in the format 09XXXXXXXXX'))
#     ])
#     biography = models.CharField(('Biography'), max_length=20, null=True, blank=True)
#     hobbies = models.CharField(('Hobbies'), choices=HOBBY_CHOICES, max_length=250, null=True, blank=True)
#     gender = models.CharField(('Gender'), choices=GENDER_CHOICES, max_length=10, null=True)
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['phone_number']
#
#     class Meta:
#         verbose_name = ('user')
#         verbose_name_plural = ('users')
#
#     def __str__(self):
#         return self.username
#
#     def save(self, *args, **kwargs):
#         self.set_password(self.password)
#         super().save(*args, **kwargs)