import pytest
from model_bakery import baker

from artists.models import Artist
from tests.utils import fake

pytestmark = pytest.mark.django_db

class TestModelArtist:
    def test_create_artist(self):
        artist = baker.make(Artist,
                           name=fake.name(),
                           band="Rock and roll",
                           alias='Crazy motherfucker')
        
        assert str(artist) == f"{artist.name} from {artist.band}, aka {artist.alias}"
