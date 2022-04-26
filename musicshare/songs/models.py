from django.db import models

from logins.models import Login


class Song(models.Model):
    name = models.CharField(max_length=155)
    logins = models.ManyToManyField(Login, 
                                    through='playlists.Playlist', 
                                    related_name='logins')
    released = models.DateField(null=True)
    single_demo = models.BooleanField(default=False)

    class Meta:
        db_table = 'songs'

    def __str__(self) -> str:
        return self.name
