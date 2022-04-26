from typing import Any

from musicshare.base import GenericDjangoListObjectField


class GenericSongListObjectField(GenericDjangoListObjectField):
    def get_queryset(self, manager, info, **kwargs) -> Any:
        return manager.all().prefetch_related('logins')
