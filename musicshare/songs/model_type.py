from graphene_django_extras import DjangoListObjectType
from graphene_django_extras import DjangoObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from songs.models import Song


DEFAULT_LIMIT = 5

class SongType(DjangoListObjectType):
    class Meta:
        model = Song
        filter_fields = {
            'name': ("iexact", "istartswith"),
        }
        pagination = LimitOffsetGraphqlPagination(default_limit=DEFAULT_LIMIT, 
                                                  ordering="-name")


class SingleSongType(DjangoObjectType):
    class Meta:
        model = Song
        filter_fields = {
            'name': ("iexact", "istartswith"),
        }
