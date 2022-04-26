from typing import Any

from musicshare.base import GenericDjangoListObjectField


class GenericArtistListObjectField(GenericDjangoListObjectField):
    def get_queryset(self, manager, info, **kwargs) -> Any:
        return manager.all()
