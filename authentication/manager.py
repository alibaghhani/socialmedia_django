from django.contrib.auth.base_user import BaseUserManager


# class UserManager(BaseUserManager):
#     def create_user(self, username,  password, phone_number,**extra_fields):
#         # if not phone_number:
#         #     raise ValueError('Phone number must be set!')
#         user = self.model(username=username, phone_number=phone_number, password=password ,**extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, username,password,phone_number, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         # extra_fields.setdefault('is_active', True)
#         user = self.create_user(username,password=password,phone_number=phone_number,**extra_fields)
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, phone_number=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username,password=password ,phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, phone_number=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, password, phone_number, **extra_fields)
