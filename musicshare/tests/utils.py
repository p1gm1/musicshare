from django.test import RequestFactory
from graphql_jwt.testcases import JSONWebTokenTestCase
from model_bakery import baker
from faker import Faker

from logins.models import Login


fake = Faker()
fake.seed()


class MusicShareTestMixin:
    """
    Has methods for creating extra entities that are useful for testing.
    """

    login = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # required for multiple inheritance
        # use self.request_factory.get(<URL>) to create a request object
        self.request_factory = RequestFactory()

    def create_login(self, **kwargs):
        kwargs.setdefault('email', fake.email())
        kwargs.setdefault('name', fake.name())
        kwargs.setdefault('enabled', True)
        password = kwargs.get('password') or fake.password()
        if password in kwargs:
            del kwargs['password']

        login = baker.make(Login, **kwargs)
        login.set_password(password)
        login._password_set_to = password
        login.save()
        self.login = self.login or login
        return login


class MusicShareTestBase(MusicShareTestMixin, JSONWebTokenTestCase):
    pass
