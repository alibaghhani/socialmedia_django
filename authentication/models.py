from django.db import models

# Create your models here.
from django.db import models
# Create your models here.
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from .manager import UserManager



class User(AbstractUser):
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
        regex=r"^(?=.*[A-Z])(?=.*\d).{8,}$",
        message="Password must be at least 8 characters long and contain at least one uppercase letter and one digit."
    )])
    phone_number = models.CharField(max_length=11, validators=[RegexValidator(
        regex=r"^09[0|1|2|3][0-9]{8}$"
    )])
    biography = models.CharField(max_length=20, default=None, null=True, blank=True)
    hobbies = models.CharField(choices=HOBBIES,max_length=250,null=True,blank=True)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=250, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number', 'password']
    objects = UserManager()

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')