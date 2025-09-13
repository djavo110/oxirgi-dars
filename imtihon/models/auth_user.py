from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self,phone_number,password = None,**extra_fields):
        if not phone_number:
            raise ValueError("Phone_number kiritilishi shart")
        user = self.model(phone_number = phone_number,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self,phone_number,password,**extra_fields):
        extra_fields.setdefault('is_admin',True)
        extra_fields.setdefault('is_staff',True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError("Superuser is_admin = True bo'lishi kerak")
        if extra_fields.setdefault('is_staff') is not True:
            raise ValueError("Superuser is_staff = True bo'lish kerak")

        return self.create_user(phone_number,password,**extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"              # login uchun maydon
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

