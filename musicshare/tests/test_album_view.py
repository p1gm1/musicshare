from model_bakery import baker

from tests.utils import MusicShareTestBase, fake
from songs.models import Song
from artists.models import Artist


class TestPlaylistView(MusicShareTestBase):
    def setUp(self):
        self.user = self.create_login(is_superuser=True)
        self.client.authenticate(self.user)
        self.song = baker.make(Song,
                               name=fake.name())
        self.artist = baker.make(Artist,
                                 name=fake.name(),
                                 alias=fake.name())

    def test_create_album(self):
        name = fake.name()
        query = """mutation {albumCreate(name:"%(name)s", 
                                         artistId:%(artist)s, 
                                         songId:%(song)s)
                                                {
                                        album{
                                                name
                                                genre
                                            }
                                        }
                                        }""" % {
                                                'name': name, 
                                                'artist': self.artist.id,
                                                'song': self.song.id
                                                }
        executed = self.client.execute(query)
        self.assertIsNone(executed.errors)
        self.assertEqual(executed.data['albumCreate']['album']['name'], name)
        