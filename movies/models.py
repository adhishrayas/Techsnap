import uuid
from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Movies(models.Model):
    id = models.UUIDField(
        default = uuid.uuid4,
        editable = False,
        primary_key = True
    )
    title = models.CharField(max_length = 255,blank = False)
    uploaded_by = models.ForeignKey(UserModel,on_delete = models.CASCADE)
    movie_file = models.FileField(upload_to='movies/')
    description = models.TextField(blank = True,null = True)
    year_of_release = models.IntegerField(blank = True,null = True)
    rating = models.IntegerField(default = 0)
    rated_by = models.IntegerField(default = 0)
    views = models.IntegerField(default = 0)

    @property
    def total_rating(self):
        if self.rated_by == 0:
            return 0
        return self.rating/self.rated_by
    
    def __str__(self):
        return self.title

class MoviesLikes(models.Model):
    id = models.UUIDField(
        default = uuid.uuid4,
        primary_key= True,
        editable = False
    )
    liked_by = models.ForeignKey(UserModel,on_delete = models.CASCADE)
    liked_on = models.ForeignKey(Movies,on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.liked_on)

class Playlists(models.Model):
    id = models.UUIDField(
        default = uuid.uuid4,
        primary_key = True,
        editable = False
    )
    title = models.CharField(max_length = 255,blank = False,null = False)
    about = models.TextField(blank = True,null = True)
    owner = models.ForeignKey(UserModel,on_delete = models.CASCADE)
    movies = models.ManyToManyField(Movies,related_name="playlists")
    is_private = models.BooleanField(default = True)
    is_highlight = models.BooleanField(default = False)
    def __str__(self):
        return f'{self.owner}:-playlist{self.title}'
