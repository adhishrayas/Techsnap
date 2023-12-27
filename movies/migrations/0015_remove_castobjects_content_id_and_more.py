# Generated by Django 5.0 on 2023-12-27 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0014_castobjects_crewobjects'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='castobjects',
            name='content_id',
        ),
        migrations.RemoveField(
            model_name='castobjects',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='crewobjects',
            name='content_id',
        ),
        migrations.RemoveField(
            model_name='crewobjects',
            name='content_type',
        ),
        migrations.AddField(
            model_name='castobjects',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='crewobjects',
            name='content',
            field=models.TextField(default=''),
        ),
    ]
