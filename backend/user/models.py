from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid


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
    username = None
    email = models.EmailField(verbose_name=_('Email'), max_length=255, unique=True)
    email_verified = models.BooleanField(verbose_name=_('Email verified'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class EmailVerification(models.Model):
    token = models.CharField(verbose_name=_('Token'), unique=True, max_length=255, default=uuid.uuid4)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
