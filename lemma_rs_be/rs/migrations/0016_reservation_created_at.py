# Generated by Django 3.2.2 on 2021-10-24 00:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rs', '0015_auto_20211022_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 10, 24, 0, 7, 1, 739303, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
