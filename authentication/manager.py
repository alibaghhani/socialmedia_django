from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number must be set!')
        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.set_password(user.password)
        user.save()
        return user

    def create_superuser(self, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, phone_number, password, **extra_fields)