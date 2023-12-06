from user.serializers import UserRetrieveSerializer


def get_me(request) -> dict:
    """Возвращает словарь с информацией о текущем пользователе."""

    return UserRetrieveSerializer(request.user).data
