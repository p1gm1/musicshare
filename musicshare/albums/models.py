from django.db import models

from musicshare.base import CharFieldChoiceEnum
from artists.models import Artist
from songs.models import Song


class AlbumGenreStatus(CharFieldChoiceEnum):
    GENRE_ROCK = 'rock'
    GENRE_JAZZ = 'jazz'
    GENRE_BLUES = 'blues'


class AlbumPopularityStatus(CharFieldChoiceEnum):
    POPULARITY_TOP = 'top'
    POPULARITY_OLDY = 'oldy'


class Album(models.Model):
    name = models.CharField(max_length=155)
    artists = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    songs = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='albums')
    genre = models.CharField(max_length=155, default=AlbumGenreStatus.GENRE_ROCK.value ,choices=AlbumGenreStatus.choices())
    popularity = models.CharField(max_length=155, default=AlbumPopularityStatus.POPULARITY_TOP.value ,choices=AlbumPopularityStatus.choices())
    
    class Meta:
        db_table = 'albums'

    def __str__(self) -> str:
        return f"{self.name} - {self.genre}"
