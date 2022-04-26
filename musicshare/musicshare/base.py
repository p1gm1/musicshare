from typing import Any, Optional
from enum import Enum

from graphql.backend.core import GraphQLCoreBackend
from graphene_django_extras import DjangoObjectField, DjangoListObjectField
from graphene_django_extras.base_types import DjangoListObjectBase
from graphene_django.utils import maybe_queryset

from musicshare.exceptions import MuscishareLoginException
from musicshare.permissions import is_authenticated


class CharFieldChoiceEnum(Enum):
    """
    A human-readable alternative to IntEnum. Includes built-in 'choice'
    functionality for django string columns.
    """
    def __str__(self):
        return self.value

    @classmethod
    def names(cls):
        return [x.name for x in cls]

    @classmethod
    def values(cls):
        return [x.value for x in cls]

    @classmethod
    def choices(cls):
        return [(x.value, x.name) for x in cls]


def auth_and_permissions(permission: str):
    def auth(f):
        def wrapper(*args, **kwargs):
            for a in args:
                try:
                    user = a.context.user
                except:
                    continue
                if user:
                    break
            
            if permission(user, **kwargs):
                return f(*args, **kwargs)
            else:
                raise MuscishareLoginException("Unauthorized request")
        return wrapper
    return auth


def measure_depth(selection_set, level=1) -> int:
    """
    Method that measures the depth of a query
    using dfs recursively, each Field in a query
    is a node of the graph.
    The graph it's called selection_set, 
    the selections property of the graphql node is
    an alias for the graph neighbour, those names are kept 
    since they're part of the vocabulary
    of graphql core.py.
    :param selection_set: Node 
    """
    max_depth = level
    for node in selection_set.selections:
        if getattr(node, "selection_set", None):
            new_depth = measure_depth(node.selection_set, level=level + 1)
            if new_depth > max_depth:
                max_depth = new_depth
    return max_depth


class DepthAnalysisBackend(GraphQLCoreBackend):
    """
    Extension of graphql backend, it overrides
    the default graphql core.py executor method 
    of a query sent by the frontend, it's purpose 
    is to get the python graph object called 
    selection_set and measure it's depth to 
    prevent a DOS attack.
    """
    def document_from_string(self, schema, document_string)  -> Any:
        document = super().document_from_string(schema, document_string)
        for graph in document.document_ast.definitions:
            depth = measure_depth(graph.selection_set)
            if depth > 5: # set your depth max here
                raise Exception('Query is too complex')

        return document


def get_object(manager, **kwargs) -> Any:
    id = kwargs.pop("id", None)
    try:
        return manager.get_queryset().get(pk=id)
    except manager.model.DoesNotExist:
        return None


def resolve_queryset(self, queryset, filterset_class, filtering_args, info ,**kwargs) -> Optional[DjangoListObjectBase]:
    filter_kwargs = {k: v for k, v in kwargs.items() if k in filtering_args}

    qs = filterset_class(data=filter_kwargs, queryset=queryset, request=info.context).qs
    count = qs.count()

    return DjangoListObjectBase(
        count=count,
        results=maybe_queryset(qs),
        results_field_name=self.type._meta.results_field_name,
    )


class GenericDjangoObjectField(DjangoObjectField):
    @staticmethod
    @auth_and_permissions(is_authenticated)
    def object_resolver(manager, root, info, **kwargs) -> Any:
        return get_object(manager, **kwargs)


class GenericDjangoListObjectField(DjangoListObjectField):
    def get_queryset(self, manager, info, **kwargs) -> Any:
        pass

    @auth_and_permissions(is_authenticated)
    def list_resolver(self, manager, filterset_class, filtering_args, root, info, **kwargs) -> Any:
        qs = self.get_queryset(manager, info ,**kwargs)
        return resolve_queryset(self, qs, filterset_class, filtering_args, info ,**kwargs)
