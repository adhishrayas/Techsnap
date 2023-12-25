from django.contrib import admin
from .models import Movies,Playlists,MoviesLikes
# Register your models here.

admin.site.register(Movies)
admin.site.register(Playlists)
admin.site.register(MoviesLikes)