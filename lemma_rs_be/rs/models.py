from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.
class AccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, fullname, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)


        return self.create_user(email, user_name, fullname, password, **other_fields)

    def create_user(self, email, user_name, fullname, password=None, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, fullname=fullname, **other_fields)
        if other_fields.get('is_superuser'):
            user.set_password(password)
        user.save()
        return user


class Resource(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    fullname = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    REQUIRED_FIELDS = ['email', 'fullname']
    USERNAME_FIELD = 'user_name'

    def __str__(self):
        return self.user_name


class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    calendar_data = models.JSONField()


class Requestor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.CharField(max_length=150, unique=True)
