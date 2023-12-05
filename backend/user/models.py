import random
import string
from typing import Any
from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    use_in_migrations = True
    
    def _create_user(self, email: str, password: str, **extra_fields) -> AbstractUser:
        if not email:
            raise ValueError(_('Users require an email field'))
        email = self.normalize_email(email)
        user: AbstractUser = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    

    def create_user(self, email: str, password: Optional[str] = None, **extra_fields) -> AbstractUser:
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    

    def create_superuser(self, email: str, password: str, **extra_fields) -> AbstractUser:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Сущность пользователя"""
    
    username = None
    email = models.EmailField(verbose_name=_('Email'), max_length=255, unique=True)
    email_verified = models.BooleanField(verbose_name=_("Email verified"), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def _repr(self) -> str:
        return self.email

    def __repr__(self) -> str:
        return self._repr()

    def __str__(self) -> str:
        return self._repr()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class ConfirmationCodeManager(models.Manager):

    def create(self, **kwargs: Any) -> Any:
        kwargs.update({'code': self._get_code()})
        return super().create(**kwargs)

    def _get_code(self) -> str:
        """Возвращает уникальный код которого нет в базе данных"""

        queryset = self.get_queryset()
        while True:
            created_code = self._get_random_code()
            if queryset.filter(code=created_code).count() == 0:
                break
        return created_code

    def _get_random_code(self, symbols: int = 6) -> str:
        """Возвращает случайный код с заданным числом символов 
        в верхнем регистре"""

        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=symbols))


class ConfirmationCode(models.Model):
    """Сущность для хранения валидный кодов 
    для верификации по email"""

    email = models.EmailField(verbose_name=_("Email"), blank=False, null=False)
    code = models.CharField(verbose_name=_('Code'), max_length=6, unique=True)
    created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)

    objects = ConfirmationCodeManager()

    def _repr(self) -> str:
        return self.code
    
    def __repr__(self) -> str:
        return self._repr()
    
    def __str__(self) -> str:
        return self._repr()
