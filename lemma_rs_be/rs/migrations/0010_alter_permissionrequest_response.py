# Generated by Django 3.2.2 on 2021-05-13 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rs', '0009_alter_permissionrequest_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissionrequest',
            name='response',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
