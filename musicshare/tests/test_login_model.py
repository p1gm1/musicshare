import pytest
from model_bakery import baker

from logins.models import Login
from tests.utils import fake

pytestmark = pytest.mark.django_db

class TestModelLogin:
    def test_create_login(self):
        login = baker.make(Login, 
                           email=fake.email(),
                           name=fake.name(),
                           enabled=True)
        login.set_password(fake.password())
        login._password_set_to = fake.password()
        login.save()

    def test_create_superuser(self):
        login = baker.make(Login, 
                           email=fake.email(),
                           name=fake.name(),
                           enabled=True,
                           is_superuser=True)
        login.set_password(fake.password())
        login._password_set_to = fake.password()
        login.save()        
        