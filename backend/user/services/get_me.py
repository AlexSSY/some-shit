from user.serializers import UserRetrieveSerializer

from .types import User


def get_me(request) -> User:
    """Возвращает словарь с информацией о текущем пользователе."""

    user = User(**UserRetrieveSerializer(request.user).data)
    return user
