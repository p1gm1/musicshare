from django.db import models

from logins.models import Login
from songs.models import Song


class Playlist(models.Model):
    name = models.CharField(max_length=155)
    logins = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='playlists')
    songs = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='playlists')
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    flag = models.CharField(max_length=155, null=True)

    class Meta:
        db_table = 'playlists'

    def __str__(self) -> str:
        return self.name
