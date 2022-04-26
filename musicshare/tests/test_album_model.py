import pytest
from model_bakery import baker

from artists.models import Artist
from songs.models import Song
from albums.models import Album
from tests.utils import fake

pytestmark = pytest.mark.django_db


class TestModelAlbum:
    def test_create_album(self):
        artist = baker.make(Artist,
                           name=fake.name(),
                           band="Rock and roll",
                           alias='Crazy motherfucker')
        song = baker.make(Song,
                          name=fake.name(),
                          released=fake.date(),)
        album = baker.make(Album,
                           name=fake.name(),
                           artists=artist,
                           songs=song,
                           genre='rock',
                           popularity='top')

        assert str(album) == f'{album.name} - {album.genre}'
        