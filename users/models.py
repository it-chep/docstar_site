from django.db import models
from django.contrib.auth.models import AbstractUser
import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import BaseUserManager, PermissionsMixin

from django.db import models


from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    email = models.EmailField('email', max_length=225, unique=True)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=255)
    verified_email = models.BooleanField(verbose_name='Email настоящий', default=False)
    email_verification_token = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'ПОЛЬЗОВАТЕЛЬ сайта'
        verbose_name_plural = 'ПОЛЬЗОВАТЕЛИ сайта'
        # ordering = ["name"]
