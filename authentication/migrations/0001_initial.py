# Generated by Django 5.0.3 on 2024-04-04 07:43

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=25, unique=True)),
                ('password', models.CharField(max_length=250, validators=[django.core.validators.RegexValidator(message='Password must be at least 8 characters long and contain at least one uppercase letter and one digit.', regex='^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[!@#$%^&*()_+])[A-Za-z\\d!@#$%^&*()_+]{8,}$')])),
                ('phone_number', models.CharField(max_length=11, null=True, validators=[django.core.validators.RegexValidator(regex='^09[0|1|2|3][0-9]{8}$')])),
                ('biography', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('hobbies', models.CharField(blank=True, choices=[('sport', '🏆'), ('music', '♫'), ('movie', '🎬'), ('sleeping', 'ᶻ 𝗓 𐰁'), ('photography', '📷')], max_length=250, null=True)),
                ('gender', models.CharField(choices=[('he', 'male'), ('she', 'female')], max_length=250, null=True)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.RegexValidator(message='enter a valid email address', regex='^([\\w]*[\\w\\.]*(?!\\.)@gmail.com)')])),
                ('profile', models.ImageField(blank=True, null=True, upload_to='media')),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]
