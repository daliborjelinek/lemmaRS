from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
from django.db.models import Max, Value
from django.db.models.functions import Coalesce
from django.utils import timezone


class DefaultSelectOrPrefetchManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self._select_related = kwargs.pop('select_related', None)
        self._prefetch_related = kwargs.pop('prefetch_related', None)

        super(DefaultSelectOrPrefetchManager, self).__init__(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super(DefaultSelectOrPrefetchManager, self).get_queryset(*args, **kwargs)

        if self._select_related:
            qs = qs.select_related(*self._select_related)
        if self._prefetch_related:
            qs = qs.prefetch_related(*self._prefetch_related)

        return qs


class Role(models.TextChoices):
    ADMIN = 'ADMIN'
    PROVIDER = 'PROVIDER'
    COMMON = 'COMMON'


class Image(models.Model):
    file = models.ImageField(upload_to='uploads/images/')


class Resource(models.Model):
    name = models.CharField(max_length=160)
    description = models.CharField(max_length=105000, default='', blank=True)
    internal_notes = models.CharField(max_length=105000, default='', blank=True)
    cost = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    image_url = models.CharField(max_length=160, default='', blank=True)
    provider = models.ForeignKey('User', on_delete=models.RESTRICT)
    tags = models.ManyToManyField('Tag', related_name='tags', blank=True)
    required_permission_level = models.ForeignKey('PermissionLevel', on_delete=models.RESTRICT)
    inv_numbers = models.JSONField(default=list)

    def not_returned(self):
        for res in self.blocking_reservations:
            if res.resource.name and res.reservation.return_date_time < timezone.now() and res.real_return_date is None and res.real_pickup_date is not None:
                return True
            pass
        return False

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=160, unique=True)

    def __str__(self):
        return self.name


class PermissionLevel(models.Model):
    name = models.CharField(max_length=160, unique=True)
    level = models.IntegerField(default=0, primary_key=True)

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

    def create_user(self, email, username, fullname, password=None, role=Role.COMMON, role_display=Role.COMMON,
                    **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, fullname=fullname, role=role, role_display=role_display,
                          **other_fields)
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
    calendar_data = models.JSONField(default=list, blank=True)
    # holidays = models.JSONField(default=list, blank=True)
    room = models.CharField(max_length=150, default="", blank=True)

    objects = AccountManager()

    REQUIRED_FIELDS = ['email', 'fullname']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.fullname

    @property
    def permission_level(self):
        return self.my_permission_requests.filter(expiration_date__gte=timezone.now()).filter(approved=True).aggregate(
            max_level=Coalesce(Max('requested_level'), Value(0))
        )['max_level']
        # self.my_permission_requests.aggregate(Max('requested_level')).filter(expiration_date__gte=datetime.now())

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
            return super().get_queryset(*args, **kwargs).filter(role=Role.PROVIDER)

    objects = ProviderObjects()

    class Meta:
        proxy = True


class CommonUser(User):
    class CommonUserObjects(models.Manager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(role=Role.COMMON)

    objects = CommonUserObjects()

    class Meta:
        proxy = True


class Admin(User):
    class AdminObjects(models.Manager):
        def get_queryset(self, *args, **kwargs):
            return super().get_queryset(*args, **kwargs).filter(role=Role.ADMIN)

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

    def __str__(self):
        return self.name


class ProjectGroup(models.Model):
    name = models.CharField(max_length=10000)
    description = models.CharField(max_length=10000, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PermissionRequest(models.Model):
    reason = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    applicant = models.ForeignKey('User', related_name='my_permission_requests', on_delete=models.PROTECT)
    approved = models.BooleanField(default=None, null=True)
    expiration_date = models.DateTimeField(null=True, default=None)
    approved_by = models.ForeignKey('User', null=True, default=None, related_name='approved_permission_request',
                                    on_delete=models.PROTECT)
    response = models.CharField(max_length=10000, blank=True, null=True)
    requested_level = models.ForeignKey('PermissionLevel', on_delete=models.PROTECT)


class Reservation(models.Model):
    project = models.ForeignKey('Project', on_delete=models.PROTECT)
    pickup_date_time = models.DateTimeField()
    return_date_time = models.DateTimeField()
    picked_up = models.BooleanField(default=False)
    applicant = models.ForeignKey('User', on_delete=models.PROTECT)
    canceled = models.BooleanField(default=False)
    approved = models.BooleanField(default=False, blank=True, null=True)
    approved_by = models.ForeignKey('User', blank=True, null=True, related_name='reservation_approved_by',
                                    on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def fully_returned(self):
        return not (self.resources.filter(real_return_date__isnull=True).count() > 0)


class ReservedResource(models.Model):
    resource = models.ForeignKey('Resource', related_name='reservations', on_delete=models.PROTECT)
    reservation = models.ForeignKey('Reservation', related_name='resources', on_delete=models.CASCADE)
    real_return_date = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=10000, blank=True, default="")
    real_pickup_date = models.DateTimeField(blank=True, null=True)

    @property
    def blocking_end(self):
        if self.reservation.pickup_date_time > timezone.now():
            # reservation not started yet
            return self.reservation.return_date_time
        if self.real_return_date is not None:
            # resource was returned
            return self.real_return_date
        if self.reservation.return_date_time > timezone.now():
            # reservation in progress
            return self.reservation.return_date_time
        if self.real_pickup_date is None:
            # reservation ended; resource was never picked up
            return self.reservation.return_date_time
        # reservation ended resource was not returned yet
        return timezone.now()
