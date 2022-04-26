from typing import Any

from musicshare.base import GenericDjangoListObjectField


class GenericAlbumListObjectField(GenericDjangoListObjectField):
    def get_queryset(self, manager, info, **kwargs) -> Any:
        return manager.all().prefetch_related('songs', 'artists')
