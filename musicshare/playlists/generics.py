from typing import Any

from musicshare.base import GenericDjangoListObjectField, auth_and_permissions
from musicshare.permissions import is_authenticated


class GenericPlaylistListObjectField(GenericDjangoListObjectField):
    def get_queryset(self, manager, info, **kwargs) -> Any:
        return manager.filter(is_public=True).prefetch_related('logins', 'songs')


class GenericPlaylistObjectField(GenericDjangoListObjectField):
    def get_queryset(self, manager, info, **kwargs) -> Any:
        name = kwargs.pop("name", None)
        try:
            return manager.get_queryset().filter(name=name)
        except manager.model.DoesNotExist:
            return None
        
