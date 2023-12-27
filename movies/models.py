import uuid
from django.db import models
from auth_modules.models import CustomUser
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Movies(models.Model):
    id = models.UUIDField(
        default = uuid.uuid4,
        editable = False,
        primary_key = True
    )
    rating = models.IntegerField(default = 0)
    rated_by = models.IntegerField(default = 0)
    content_id = models.IntegerField(default = 0)
    title = models.CharField(max_length = 255,default = '')
    tagline = models.TextField(default = '')
    release_date = models.CharField(max_length = 255,default = '')
    runtime = models.CharField(max_length = 255,default = '')
    overview = models.TextField(default = '')
    budget = models.CharField(max_length = 255,default = '')
    status = models.CharField(max_length = 255,default = '')
    country = models.CharField(max_length = 255,default = '')
    revenue = models.CharField(max_length = 255,default = '')
    language = models.CharField(max_length = 255,default = '')
    content_type = models.CharField(max_length = 255,default ='')
    trailer_link = models.CharField(max_length = 255,default = '')
    genre = models.TextField(default = '')
    production_companies = models.TextField(default = '')
    @property
    def total_rating(self):
        if self.rated_by == 0:
            return 0
        return self.rating/self.rated_by
    
    def __str__(self):
        return str(self.content_id)

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

class MoviesDisLikes(models.Model):
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

class Ratings(models.Model):
    id = models.UUIDField(
        default = uuid.uuid4,
        primary_key = True,
        editable = False
    )
    rating = models.IntegerField(default = 0)
    rated_by = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
    rated_on = models.ForeignKey(Movies,on_delete = models.CASCADE)

class Reaction(models.Model):
    id = models.UUIDField(
        default = uuid.uuid4,
        primary_key = True,
        editable =False,
    )
    reaction = models.IntegerField(default = 0)
    reacted_by = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
    reacted_on = models.ForeignKey(Movies,on_delete = models.CASCADE)

class TrackObject(models.Model):
    id = models.UUIDField(
        default = uuid.uuid4,
        primary_key = True,
        editable = False,
    )
    content_id = models.IntegerField(default = 0)
    episode = models.IntegerField(default = 0)
    owner = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
    season = models.IntegerField(default = 0)
    title = models.CharField(max_length = 255,blank = True,null = True)
    synopsis = models.TextField(blank = True,null =True)
    show = models.CharField(max_length = 255,blank = True,null = True)


class CastObjects(models.Model):
    id = models.UUIDField(
        default = uuid.uuid4,
        primary_key = True,
        editable = False,
    )
    content = models.TextField(default = '')
    name = models.CharField(max_length = 255,blank = True,null = True)

class CrewObjects(models.Model):
    id = models.UUIDField(
        default = uuid.uuid4,
        primary_key = True,
        editable = False,
    )
    name = models.CharField(max_length = 255,blank = True,null = True)
    content = models.TextField(default = '')
    