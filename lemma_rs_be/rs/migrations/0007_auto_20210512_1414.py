# Generated by Django 3.2.2 on 2021-05-12 12:14

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rs', '0006_auto_20210512_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissionrequest',
            name='approved_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='approved_permission_request', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='permissionrequest',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 12, 14, 47, 977707, tzinfo=utc)),
        ),
    ]
