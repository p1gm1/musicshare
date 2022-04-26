from os import name
import pytest
from model_bakery import baker

from songs.models import Song
from playlists.models import Playlist
from tests.utils import fake, MusicShareTestBase


pytestmark = pytest.mark.django_db

class TestModelSong(MusicShareTestBase):
    def test_create_song(self):
        song = baker.make(Song,
                          name=fake.name(),
                          released=fake.date(),
                          )
        
        assert str(song) == song.name

    def test_playlist_song(self):
        login = self.create_login()
        song = baker.make(Song,
                          name=fake.name(),
                          released=fake.date(),
                          )
        playlist = baker.make(Playlist,
                              name=fake.name(),
                              logins=login,
                              songs=song)

        assert song.logins.first() == login
        assert str(playlist) == playlist.name
