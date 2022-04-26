from graphene_django_extras import DjangoListObjectType
from graphene_django_extras import DjangoObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from playlists.models import Playlist


DEFAULT_LIMIT = 5

class PlaylistType(DjangoListObjectType):
    class Meta:
        model = Playlist
        filter_fields = {
            'name': ("iexact", "istartswith"),
            'flag': ("iexact", "istartswith"),
        }
        pagination = LimitOffsetGraphqlPagination(default_limit=DEFAULT_LIMIT, 
                                                  ordering="-name")


class SinglePlaylistType(DjangoObjectType):
    class Meta:
        model = Playlist
        filter_fields = {
            'name': ("iexact", "istartswith"),
            'flag': ("iexact", "istartswith"),
        }
