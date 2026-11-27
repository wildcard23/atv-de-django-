from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class EmailUserManager(BaseUserManager):
    use_in_migrations = True

    def normalize_email(self, email):
        return super().normalize_email(email).lower()

    def get_by_natural_key(self, username):
        return self.get(email__iexact=username)

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório.')
        if not username:
            raise ValueError('O nome de usuário é obrigatório.')
        user = self.model(
            email=self.normalize_email(email),
            username=self.model.normalize_username(username),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuários precisam ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuários precisam ter is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField('e-mail', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = EmailUserManager()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
