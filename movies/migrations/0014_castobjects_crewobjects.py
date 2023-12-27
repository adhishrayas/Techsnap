# Generated by Django 5.0 on 2023-12-27 12:12

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_trackobject_show'),
    ]

    operations = [
        migrations.CreateModel(
            name='CastObjects',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content_id', models.IntegerField(default=0)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('content_type', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CrewObjects',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content_id', models.IntegerField(default=0)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('content_type', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]