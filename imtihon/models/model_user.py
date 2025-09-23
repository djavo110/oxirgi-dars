from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import random
import datetime
from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email kiritilishi shart")
        email = self.normalize_email(email)  # emailni standartlashtiradi
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError("Superuser is_admin=True bo‘lishi kerak")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser is_staff=True bo‘lishi kerak")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"              # login uchun maydon
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone_number) if self.phone_number else str(self.email)

class EmailOTP(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):
        """6 xonali tasodifiy OTP kod yaratadi"""
        code = str(random.randint(100000, 999999))
        self.otp = code
        self.created_at = timezone.now()
        self.save()
        return code

    def is_valid(self):
        """OTP 5 daqiqa amal qiladi"""
        return timezone.now() < self.created_at + datetime.timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"

