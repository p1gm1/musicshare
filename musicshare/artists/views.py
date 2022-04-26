import graphene
from graphql_auth.bases import Output, DynamicArgsMixin

from artists.model_type import SingleArtistType, ArtistType
from artists.models import Artist
from artists.generics import GenericArtistListObjectField
from musicshare.base import GenericDjangoObjectField, auth_and_permissions
from musicshare.permissions import is_admin


class ArtistQuery(graphene.ObjectType):
    artists = GenericArtistListObjectField(ArtistType)
    artist = GenericDjangoObjectField(SingleArtistType, 
                                      id=graphene.Int(required=True))


class ArtistCreate(Output, DynamicArgsMixin, graphene.Mutation):
    _required_args={
        'name': 'String',
        'alias': 'String',
    }
    _args={
        'band': 'String',
        'instrument': 'String',
        'status': 'String',
    }
    
    artist = graphene.Field(SingleArtistType)

    @classmethod
    @auth_and_permissions(is_admin)
    def mutate(cls, root, info, **kwargs):
        artist, _ = Artist.objects.get_or_create(**kwargs)
        assert isinstance(artist, Artist)
        return cls(artist=artist)


class ArtistUpdate(Output, DynamicArgsMixin, graphene.Mutation):
    _required_args={
        'id': 'ID',
    }
    _args={
        'name': 'String',
        'alias': 'String',
        'band': 'String',
        'instrument': 'String',
        'status': 'String',
    }
    
    artist = graphene.Field(SingleArtistType)

    @classmethod
    @auth_and_permissions(is_admin)
    def mutate(cls, root, info, **kwargs):
        id = kwargs.pop('id', None)
        Artist.objects.filter(id=id).update(**kwargs)
        artist = Artist.objects.get(id=id)
        assert isinstance(artist, Artist)
        return cls(artist=artist)


class ArtistDelete(Output, DynamicArgsMixin, graphene.Mutation):
    _required_args={
        'id': 'ID',
    }
    
    artist = graphene.Field(SingleArtistType)

    @classmethod
    @auth_and_permissions(is_admin)
    def mutate(cls, root, info, **kwargs):
        id = kwargs.pop('id', None)
        artist = Artist.objects.get(id=id)
        Artist.objects.filter(id=id).delete()
        assert isinstance(artist, Artist)
        return cls(artist=artist)


class ArtistMutation(graphene.ObjectType):
    artist_create = ArtistCreate.Field()
    artist_update = ArtistUpdate.Field()
    artist_delete = ArtistDelete.Field()
