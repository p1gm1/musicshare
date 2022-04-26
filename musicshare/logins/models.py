from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import EmailValidator
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.password_validation import password_changed, validate_password
from django.db import models


class LoginManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        validate_email = EmailValidator('Invalid email provided')
        email = self.normalize_email(email)
        validate_email(email)
        user = self.model(email=email, **extra_fields)
        validate_password(password, user)
        user.set_password(password)
        user.save(using=self._db)
        password_changed(password, user)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{f'{self.model.USERNAME_FIELD}__iexact': username})


class Login(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(db_column='password_hashed', max_length=128)
    name = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = LoginManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'logins'
