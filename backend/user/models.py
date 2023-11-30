from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
    pass


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name=_('Email'), max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meata:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
