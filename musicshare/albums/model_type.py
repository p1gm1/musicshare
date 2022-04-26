from graphene_django_extras import DjangoListObjectType
from graphene_django_extras import DjangoObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from albums.models import Album


DEFAULT_LIMIT = 5

class AlbumType(DjangoListObjectType):
    class Meta:
        model = Album
        filter_fields = {
            'name': ("iexact", "istartswith"),
            'genre': ("iexact", "istartswith"),
            'popularity': ("exact", ),
        }
        pagination = LimitOffsetGraphqlPagination(default_limit=DEFAULT_LIMIT, 
                                                  ordering="-name")


class SingleAlbumType(DjangoObjectType):
    class Meta:
        model = Album
        filter_fields = {
            'name': ("iexact", "istartswith"),
            'genre': ("iexact", "istartswith"),
            'popularity': ("exact", ),
        }
