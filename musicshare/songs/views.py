import graphene
from graphql_auth.bases import Output, DynamicArgsMixin

from logins.models import Login
from songs.models import Song
from songs.model_type import SingleSongType, SongType
from songs.generics import GenericSongListObjectField
from musicshare.base import GenericDjangoObjectField, auth_and_permissions
from musicshare.permissions import is_admin


class SongQuery(graphene.ObjectType):
    songs = GenericSongListObjectField(SongType)
    song = GenericDjangoObjectField(SingleSongType, 
                                      id=graphene.Int(required=True))


class SongCreate(Output, DynamicArgsMixin, graphene.Mutation):
    _required_args = {
        'name': 'String',
        'login_id': 'ID',
    }

    song = graphene.Field(SingleSongType)

    @classmethod
    @auth_and_permissions(is_admin)
    def mutate(cls, root, info, **kwargs):
        kwargs['logins'] = Login.objects.get(id=kwargs.pop('login_id'))
        song, _ = Song.objects.get_or_create(**kwargs)
        assert isinstance(song, Song)
        return cls(song=song)



class SongUpdate(Output, DynamicArgsMixin, graphene.Mutation):
    _required_args = {
        'id': 'ID',
        'name': 'String',
        'login_id': 'ID',
    }

    song = graphene.Field(SingleSongType)

    @classmethod
    @auth_and_permissions(is_admin)
    def mutate(cls, root, info, **kwargs):
        kwargs['logins'] = Login.objects.get(id=kwargs.pop('login_id'))
        id = kwargs.pop('id')
        Song.objects.filter(id=id).update(**kwargs)
        song = Song.objects.get(id=id) 
        return cls(song=song)


class SongDelete(Output, DynamicArgsMixin, graphene.Mutation):
    _required_args = {
        'id': 'ID',
    }

    song = graphene.Field(SingleSongType)    

    @classmethod
    @auth_and_permissions(is_admin)
    def mutate(cls, root, info, **kwargs):
        id = kwargs.pop('id')
        song = Song.objects.get(id=id)
        Song.objects.filter(id=kwargs.pop('id')).delete()
        return cls(song=song)


class SongMutation(graphene.ObjectType):
    song_create = SongCreate.Field()
    song_update = SongUpdate.Field()
    song_update = SongDelete.Field()
