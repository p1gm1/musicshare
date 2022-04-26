from graphene_django_extras import DjangoListObjectType
from graphene_django_extras import DjangoObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

from artists.models import Artist


DEFAULT_LIMIT = 5

class ArtistType(DjangoListObjectType):
    class Meta:
        model = Artist
        filter_fields = {
            'name': ("iexact", "istartswith"),
            'alias': ("iexact", "istartswith"),
            'band': ("exact", ),
        }
        pagination = LimitOffsetGraphqlPagination(default_limit=DEFAULT_LIMIT, 
                                                  ordering="-name")


class SingleArtistType(DjangoObjectType):
    class Meta:
        model = Artist
        filter_fields = {
            'name': ("iexact", "istartswith"),
            'alias': ("iexact", "istartswith"),
            'band': ("exact", ),
        }
