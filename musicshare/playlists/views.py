import graphene
from graphql_auth.bases import Output, DynamicArgsMixin

from musicshare.base import auth_and_permissions
from musicshare.permissions import is_authenticated
from musicshare.exceptions import MuscishareLoginException
from playlists.model_type import PlaylistType, SinglePlaylistType
from playlists.generics import GenericPlaylistObjectField, GenericPlaylistListObjectField
from playlists.models import Playlist
from songs.models import Song
from logins.models import Login


class PlaylistQuery(graphene.ObjectType):
    playlists = GenericPlaylistListObjectField(PlaylistType)
    playlist = GenericPlaylistObjectField(PlaylistType, 
                                          name=graphene.String(required=True))


class PlaylistCreate(Output, DynamicArgsMixin, graphene.Mutation):
    _required_args={
        'name': 'String',
        'logins_id': 'ID',
        'songs_id': 'ID',
    }
    _args={
        'is_public': 'Boolean',
        'active': 'Boolean',
        'flag': 'String'
    }
    
    playlist = graphene.Field(SinglePlaylistType)

    @classmethod
    @auth_and_permissions(is_authenticated)
    def mutate(cls, root, info, **kwargs):
        kwargs['songs'] = Song.objects.get(id=kwargs.pop('songs_id'))
        kwargs['logins'] = Login.objects.get(id=kwargs.pop('logins_id'))
        playlist, _ = Playlist.objects.get_or_create(**kwargs)
        assert isinstance(playlist, Playlist)
        return cls(playlist=playlist)


class PlaylistUpdate(Output, DynamicArgsMixin, graphene.Mutation):
    _required_args={
        'id': 'ID',
        'name': 'String',
        'logins_id': 'ID',
        'songs_id': 'ID',
    }
    _args={
        'is_public': 'Boolean',
        'active': 'Boolean',
        'flag': 'String'
    }
    
    playlist = graphene.Field(SinglePlaylistType)

    @classmethod
    @auth_and_permissions(is_authenticated)
    def mutate(cls, root, info, **kwargs):
        if info.context.user == Playlist.objects.get(id=kwargs.get('id')).logins:
            id = kwargs.pop('id', None)
            playlist = Playlist.objects.get(id=id)
            kwargs['songs'] = Song.objects.get(id=kwargs.pop('songs_id'))
            kwargs['logins'] = Login.objects.get(id=kwargs.pop('logins_id'))
            Playlist.objects.filter(id=id).update(**kwargs)
            return cls(playlist=playlist)
        else:
            raise MuscishareLoginException("You can't edit that playlist")


class PlaylistDelete(Output, DynamicArgsMixin, graphene.Mutation):
    _required_args={
        'id': 'ID',
    }
    
    playlist = graphene.Field(SinglePlaylistType)

    @classmethod
    @auth_and_permissions(is_authenticated)
    def mutate(cls, root, info, **kwargs):
        if info.context.user == Playlist.objects.get(id=kwargs.get('id')).logins:
            id = kwargs.pop('id', None)
            playlist = Playlist.objects.get(id=id)
            Playlist.objects.filter(id=id).delete()
            return cls(playlist=playlist)
        else:
            raise MuscishareLoginException("You can't edit that playlist")


class PlaylistMutation(graphene.ObjectType):
    playlist_create = PlaylistCreate.Field()
    playlist_update = PlaylistUpdate.Field()
    playlist_delete = PlaylistDelete.Field()
