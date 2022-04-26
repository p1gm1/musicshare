from graphene import Enum


class AlbumGenreGrapheneStatus(Enum):
    ROCK = 'rock'
    JAZZ = 'jazz'
    BLUES = 'blues'


class AlbumPopularityGrapheneStatus(Enum):
    TOP = 'top'
    OLDY = 'oldy'
    