from django.utils import timezone
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token as AuthToken

from user.models import User


def get_auth_token(request) -> str:
    """Возвращает токен для авторизации запросов."""

    user = _get_user_by_email_and_password(request)
    token, is_created = AuthToken.objects.get_or_create(user=user)
    _update_user_last_login(user)
    return token.key


def _get_user_by_email_and_password(request) -> User:
    """Возвращает пользователя по email & password."""

    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data['user']


def _update_user_last_login(user) -> None:
    """Обновляет поле last_login пользователя."""
    
    user.last_login = timezone.now()
    user.save()
