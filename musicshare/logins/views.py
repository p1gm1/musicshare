from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager
from django.core.validators import EmailValidator
from django.contrib.auth.password_validation import validate_password
import graphene
import graphql_jwt
from graphql_auth import mutations
from graphql_auth.mixins import ObtainJSONWebTokenMixin
from graphql_auth.schema import UserNode


def validate_credentials(f):
    def wrapper(*args, **kwargs):
        user = args[2].context.user
        password = kwargs.get('password')
        email = kwargs.get('email')
        validate_email = EmailValidator('Invalid email provided')
        email = BaseUserManager.normalize_email(email)
        validate_email(email)
        validate_password(password, user)
        return f(*args, **kwargs)
    return wrapper


class MutationMixin:
    """
    Custom class for login
    """

    @classmethod
    @validate_credentials
    def mutate(cls, root, info, **input):
        return cls.resolve_mutation(root, info, **input)

    @classmethod
    def parent_resolve(cls, root, info, **kwargs):
        return super().mutate(root, info, **kwargs)


class CustomObtainJSONWebToken(MutationMixin, 
                               ObtainJSONWebTokenMixin, 
                               graphql_jwt.JSONWebTokenMutation):
    __doc__ = ObtainJSONWebTokenMixin.__doc__
    user = graphene.Field(UserNode)
    unarchiving = graphene.Boolean(default_value=False)

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update({"password": graphene.String(required=True)})
        for field in settings.GRAPHQL_AUTH['LOGIN_ALLOWED_FIELDS']:
            cls._meta.arguments.update({field: graphene.String()})
        return super(graphql_jwt.JSONWebTokenMutation, cls).Field(*args, **kwargs)


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    token_auth = CustomObtainJSONWebToken.Field()
    refresh_token = mutations.RefreshToken.Field()
