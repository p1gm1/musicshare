from model_bakery import baker

from tests.utils import MusicShareTestBase, fake
from songs.models import Song
from playlists.models import Playlist


class TestPlaylistView(MusicShareTestBase):
    def setUp(self):
        self.user = self.create_login()
        self.client.authenticate(self.user)
        self.song = baker.make(Song,
                               name=fake.name())
        self.playlist = baker.make(Playlist,
                             name=fake.name(),
                             logins=self.user,
                             songs=self.song,
                             is_public=True)

    def test_read_playlists(self):
        song = baker.make(Song,
                   name=fake.name())
        baker.make(Playlist,
                   name=self.playlist.name,
                   logins=self.user,
                   songs=song)
        query = """query {playlists {
                            results {
                                name
                            }    
            }
        }"""
        executed = self.client.execute(query)
        self.assertIsNone(executed.errors)
        self.assertEqual(len(executed.data['playlists']['results']), 1)
        self.assertEqual(executed.data['playlists']['results'][0]['name'], 
                         self.playlist.name)

    def test_show_playlist(self):
        query = """query {playlist(name: "%s") {
                            results {
                                name
                            }
            }
        }""" % self.playlist.name
        executed = self.client.execute(query)
        self.assertIsNone(executed.errors)

        self.assertEqual(executed.data['playlist']['results'][0]['name'], 
                         self.playlist.name)

    def test_create_playlist(self):
        name = fake.name()
        query = """mutation {playlistCreate(name:"%(name)s", 
                                            isPublic: true,
                                            flag: "chill", 
                                            loginsId:%(user)s,
                                            songsId:%(song)s) {
                                        playlist {
                                                name
                                                isPublic
                                            }
                                        }
                                        }""" % {
                                                'name': name, 
                                                'user': self.user.id,
                                                'song': self.song.id
                                                }
        executed = self.client.execute(query)
        self.assertIsNone(executed.errors)

        self.assertEqual(executed.data['playlistCreate']['playlist']['name'], name)

    def test_update_playlist(self):
        name = fake.name()
        query = """mutation {playlistUpdate(id: %(id)s,
                                            name:"%(name)s", 
                                            isPublic: true,
                                            flag: "chill", 
                                            loginsId:%(user)s,
                                            songsId:%(song)s) {
                                        playlist {
                                                name
                                                isPublic
                                            }
                                        }
                                        }""" % {
                                                'id': self.playlist.id,
                                                'name': name, 
                                                'user': self.user.id,
                                                'song': self.song.id
                                                }
        executed = self.client.execute(query)
        self.assertIsNone(executed.errors)

        self.assertEqual(executed.data['playlistUpdate']['playlist']['name'], self.playlist.name)

    def test_delete_playlist(self):
        query = """mutation {playlistDelete(id: %(id)s) {
                                        playlist {
                                                name
                                                isPublic
                                            }
                                        }
                                        }""" % {
                                                'id': self.playlist.id,
                                                }
        executed = self.client.execute(query)
        self.assertIsNone(executed.errors)
        self.assertEqual(executed.data['playlistDelete']['playlist']['name'], self.playlist.name)
        