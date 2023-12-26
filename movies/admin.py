from django.contrib import admin
from .models import Movies,Playlists,MoviesLikes,TrackObject,Ratings,Reaction
# Register your models here.

admin.site.register(Movies)
admin.site.register(Playlists)
admin.site.register(MoviesLikes)
admin.site.register(TrackObject)
admin.site.register(Ratings)
admin.site.register(Reaction)