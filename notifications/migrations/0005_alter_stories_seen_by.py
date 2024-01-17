# Generated by Django 5.0 on 2024-01-17 13:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_reportedblogs_stories'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='seen_by',
            field=models.ManyToManyField(blank=True, null=True, related_name='seen_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
