from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.

class Role(models.TextChoices):
    ADMIN = 'ADMIN'
    PROVIDER = 'PROVIDER'
    COMMON = 'COMMON'

class Resource(models.Model):
    name = models.CharField(max_length=160)
    description = models.CharField(max_length=5000, default='')
    internalNotes = models.CharField(max_length=5000, default='')
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='uploads/resources/', blank=True)
    provider = models.ForeignKey('Provider', on_delete=models.RESTRICT)
    tags = models.ManyToManyField('Tag', related_name='tags', blank=True)
    requiredPermissionLevel = models.ForeignKey('PermissionLevel',on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=160)

    def __str__(self):
        return self.name

class PermissionLevel(models.Model):
    name = models.CharField(max_length=160, unique=True)

def __str__(self):
    return self.name


class AccountManager(BaseUserManager):

    def create_superuser(self, email, username, fullname, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('role', Role.ADMIN)
        other_fields.setdefault('role_display', Role.ADMIN)

        return self.create_user(email, username, fullname, password, **other_fields)

    def create_user(self, email, username, fullname, password=None, role=Role.COMMON, role_display=Role.COMMON, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, fullname=fullname, role=role, role_display=role_display, **other_fields)
        if other_fields.get('is_superuser'):
            user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField('password', max_length=128, blank=True)
    fullname = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(choices=Role.choices, max_length=50, default=Role.COMMON)
    role_display = models.CharField(choices=Role.choices, max_length=50, default=Role.COMMON)
    address = models.CharField(max_length=150, default="", blank=True)
    calendar_data = models.JSONField(default=dict, blank=True)
    room = models.CharField(max_length=150, default="", blank=True)

    objects = AccountManager()

    REQUIRED_FIELDS = ['email', 'fullname']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_Role_valid",
                check=models.Q(role__in=Role.values),
            )
        ]


class Provider(User):
    class ProviderObjects(models.Manager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(role=User.Role.PROVIDER)

    objects = ProviderObjects()

    class Meta:
        proxy = True


class CommonUser(User):
    class CommonUserObjects(models.Manager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(role=User.Role.COMMON)

    objects = CommonUserObjects()

    class Meta:
        proxy = True


class Admin(User):
    class AdminObjects(models.Manager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(role=User.Role.ADMIN)

    objects = AdminObjects()

    class Meta:
        proxy = True


class Project(models.Model):
    name = models.CharField(max_length=10000)
    description = models.CharField(max_length=10000, blank=True)
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('User', on_delete=models.PROTECT)
    members = models.ManyToManyField(User, related_name='members', blank=True)
    group = models.ForeignKey('ProjectGroup', on_delete=models.PROTECT)


class ProjectGroup(models.Model):
    name = models.CharField(max_length=10000)
    description = models.CharField(max_length=10000, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


