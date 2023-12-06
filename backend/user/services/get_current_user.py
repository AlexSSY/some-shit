from user.serializers import UserRetrieveSerializer

from .types import UserDict


def get_current_user(request) -> UserDict:
    """Возвращает словарь с информацией о текущем пользователе."""

    user = UserDict(**UserRetrieveSerializer(request.user).data)
    return user
