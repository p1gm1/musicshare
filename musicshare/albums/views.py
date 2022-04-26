import graphene
from graphql_auth.bases import Output, DynamicArgsMixin

from albums.models import Album
from songs.models import Song
from artists.models import Artist
from albums.model_type import SingleAlbumType, AlbumType
from albums.generics import GenericAlbumListObjectField
from musicshare.base import GenericDjangoObjectField, auth_and_permissions
from musicshare.permissions import is_admin


class AlbumQuery(graphene.ObjectType):
    albums = GenericAlbumListObjectField(AlbumType)
    album = GenericDjangoObjectField(SingleAlbumType, 
                                      id=graphene.Int(required=True))


class AlbumCreate(Output, DynamicArgsMixin, graphene.Mutation):
    _required_args = {
        'name': 'String',
        'artist_id': 'ID',
        'song_id': 'ID',
    }

    album = graphene.Field(SingleAlbumType)

    @classmethod
    @auth_and_permissions(is_admin)
    def mutate(cls, root, info, **kwargs):
        kwargs['artists'] = Artist.objects.get(id=kwargs.pop('artist_id'))
        kwargs['songs'] = Song.objects.get(id=kwargs.pop('song_id'))
        album, _ = Album.objects.get_or_create(**kwargs)
        assert isinstance(album, Album)
        return cls(album=album)


class AlbumUpdate(Output, DynamicArgsMixin, graphene.Mutation):
    _required_args = {
        'id': 'ID',
        'artist_id': 'ID',
        'song_id': 'ID',
    }
    _args={
        'name': 'String',
    }

    album = graphene.Field(SingleAlbumType)

    @classmethod
    @auth_and_permissions(is_admin)
    def mutate(cls, root, info, **kwargs):
        id = kwargs.pop('id', None)
        kwargs['artists'] = Artist.objects.get(id=kwargs.pop('artist_id'))
        kwargs['songs'] = Song.objects.get(id=kwargs.pop('song_id'))
        Album.objects.filter(id=id).update(**kwargs)
        album = Album.objects.get(id=id)
        return cls(album=album)


class AlbumDelete(Output, DynamicArgsMixin, graphene.Mutation):
    _required_args = {
        'id': 'ID',
    }

    album = graphene.Field(SingleAlbumType)

    @classmethod
    @auth_and_permissions(is_admin)
    def mutate(cls, root, info, **kwargs):
        id = kwargs.pop('id', None)
        album = Album.objects.get(id=id)
        Album.objects.filter(id=id).delete()
        return cls(album=album)


class AlbumMutation(graphene.ObjectType):
    album_create = AlbumCreate.Field()
    album_update = AlbumUpdate.Field()
    album_update = AlbumDelete.Field()
