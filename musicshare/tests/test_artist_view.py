from model_bakery import baker

from tests.utils import MusicShareTestBase, fake
from artists.models import Artist


class TestArtistView(MusicShareTestBase):
    def setUp(self):
        self.user = self.create_login(is_superuser=True)
        self.client.authenticate(self.user)
        self.artist = baker.make(Artist,
                           name=fake.name(),
                           band="Rock and roll",
                           alias='Crazy motherfucker')

    def test_read_artists(self):
        artist = baker.make(Artist,
                           name=fake.name(),
                           band="Rock and roll",
                           alias='Lil peep')
        query = """query {artists {
                            results {
                                name
                                alias
                                band
                                instrument
                                status
                            }    
            }
        }"""
        executed = self.client.execute(query)
        self.assertIsNone(executed.errors)
        
        self.assertIn(executed.data['artists']['results'][0]['name'], (artist.name, self.artist.name))
        self.assertIn(executed.data['artists']['results'][1]['name'], (artist.name, self.artist.name))
        self.assertIn(executed.data['artists']['results'][0]['alias'],(artist.alias, self.artist.alias))
        self.assertIn(executed.data['artists']['results'][1]['alias'], (artist.alias, self.artist.alias))
        self.assertIn(executed.data['artists']['results'][0]['band'], (artist.band, self.artist.band))
        self.assertIn(executed.data['artists']['results'][1]['band'], (artist.band, self.artist.band))

    def test_show_artist(self):
        query = """query {artist(id: %s) {
                                name
                                alias
                                band
                                instrument
                                status
            }
        }""" % self.artist.id
        executed = self.client.execute(query)
        self.assertIsNone(executed.errors)
        
        self.assertEqual(executed.data['artist']['name'], self.artist.name)
        self.assertEqual(executed.data['artist']['alias'], self.artist.alias)
        self.assertEqual(executed.data['artist']['band'], self.artist.band)

    def test_create_artist(self):
        name = fake.name()
        alias = "MGK"
        band = "Machine Gun Kelly"
        query = """mutation {artistCreate(name:"%(name)s", 
                                          alias:"%(alias)s", 
                                          band:"%(band)s",
                                          instrument: "chello") {
  											artist {
                                                   name
                                                   alias
                                                   band 
                                                }
	                                        }
                                        }""" % {
                                                'name': name, 
                                                'alias': alias,
                                                'band': band
                                                }
        executed = self.client.execute(query)
        self.assertIsNone(executed.errors)

        self.assertEqual(executed.data['artistCreate']['artist']['name'], name)
        self.assertEqual(executed.data['artistCreate']['artist']['alias'], alias)
        self.assertEqual(executed.data['artistCreate']['artist']['band'], band)

    def test_mutation_badrequest(self):
        user = self.create_login()
        self.client.authenticate(user)
        name = fake.name()
        alias = "MGK"
        band = "Machine Gun Kelly"
        query = """mutation {artistCreate(name:"%(name)s", 
                                          alias:"%(alias)s", 
                                          band:"%(band)s",
                                          instrument: "chello") {
  											artist {
                                                   name
                                                   alias
                                                   band 
                                                }
	                                        }
                                        }""" % {
                                                'name': name, 
                                                'alias': alias,
                                                'band': band
                                                }
        executed = self.client.execute(query)
        self.assertIsNotNone(executed.errors)
        
    def test_update_artist(self):
        name = fake.name()
        alias = "MGK"
        band = "Machine Gun Kelly"
        query = """mutation {artistUpdate(id: %(id)s,
                                          name:"%(name)s", 
                                          alias:"%(alias)s", 
                                          band:"%(band)s",
                                          instrument: "chello") {
  											artist {
                                                   name
                                                   alias
                                                   band 
                                                }
	                                        }
                                        }""" % {
                                                'id': self.artist.id,
                                                'name': name, 
                                                'alias': alias,
                                                'band': band
                                                }
        executed = self.client.execute(query)
        self.assertIsNone(executed.errors)

        self.assertEqual(executed.data['artistUpdate']['artist']['name'], name)
        self.assertEqual(executed.data['artistUpdate']['artist']['alias'], alias)
        self.assertEqual(executed.data['artistUpdate']['artist']['band'], band)

    def test_delete_artist(self):
        query = """mutation {artistDelete(id: %(id)s) {
  											artist {
                                                   name
                                                   alias
                                                   band 
                                                }
	                                        }
                                        }""" % {
                                                'id': self.artist.id,
                                                }
        executed = self.client.execute(query)
        self.assertIsNone(executed.errors)

        self.assertEqual(executed.data['artistDelete']['artist']['name'], 
                         self.artist.name)
