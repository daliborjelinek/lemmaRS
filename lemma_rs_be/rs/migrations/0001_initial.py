# Generated by Django 3.2.2 on 2021-10-31 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(blank=True, max_length=128, verbose_name='password')),
                ('fullname', models.CharField(blank=True, max_length=150)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('ADMIN', 'Admin'), ('PROVIDER', 'Provider'), ('COMMON', 'Common')], default='COMMON', max_length=50)),
                ('role_display', models.CharField(choices=[('ADMIN', 'Admin'), ('PROVIDER', 'Provider'), ('COMMON', 'Common')], default='COMMON', max_length=50)),
                ('address', models.CharField(blank=True, default='', max_length=150)),
                ('calendar_data', models.JSONField(blank=True, default=dict)),
                ('room', models.CharField(blank=True, default='', max_length=150)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='uploads/images/')),
            ],
        ),
        migrations.CreateModel(
            name='PermissionLevel',
            fields=[
                ('name', models.CharField(max_length=160, unique=True)),
                ('level', models.IntegerField(default=0, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10000)),
                ('description', models.CharField(blank=True, max_length=10000)),
                ('finished', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10000)),
                ('description', models.CharField(blank=True, max_length=10000)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_date_time', models.DateTimeField()),
                ('return_date_time', models.DateTimeField()),
                ('picked_up', models.BooleanField(default=False)),
                ('canceled', models.BooleanField(default=False)),
                ('approved', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reservation_approved_by', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rs.project')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('description', models.CharField(blank=True, default='', max_length=105000)),
                ('internal_notes', models.CharField(blank=True, default='', max_length=105000)),
                ('cost', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('image_url', models.CharField(blank=True, default='', max_length=160)),
                ('inv_numbers', models.JSONField(default=list)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('required_permission_level', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='rs.permissionlevel')),
                ('tags', models.ManyToManyField(blank=True, related_name='tags', to='rs.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='ReservedResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_return_date', models.DateTimeField(blank=True, null=True)),
                ('comment', models.CharField(blank=True, default='', max_length=10000)),
                ('real_pickup_date', models.DateTimeField(blank=True, null=True)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='rs.reservation')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reservations', to='rs.resource')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rs.projectgroup'),
        ),
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='PermissionRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=10000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=None, null=True)),
                ('expiration_date', models.DateTimeField(default=None, null=True)),
                ('response', models.CharField(blank=True, max_length=10000, null=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='my_permission_requests', to=settings.AUTH_USER_MODEL)),
                ('approved_by', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='approved_permission_request', to=settings.AUTH_USER_MODEL)),
                ('requested_level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rs.permissionlevel')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('rs.user',),
        ),
        migrations.CreateModel(
            name='CommonUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('rs.user',),
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('rs.user',),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(('role__in', ['ADMIN', 'PROVIDER', 'COMMON'])), name='rs_user_Role_valid'),
        ),
    ]
