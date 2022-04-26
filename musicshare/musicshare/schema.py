import graphene

from logins.views import AuthMutation
from artists.views import ArtistQuery, ArtistMutation
from albums.views import AlbumQuery, AlbumMutation
from songs.views import SongQuery, SongMutation
from playlists.views import PlaylistQuery, PlaylistMutation


class Query(AlbumQuery, ArtistQuery, SongQuery, 
            PlaylistQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, ArtistMutation, PlaylistMutation,
               AlbumMutation, SongMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
