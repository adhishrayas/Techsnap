# Generated by Django 5.0 on 2023-12-20 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_playlists_is_highlight'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]