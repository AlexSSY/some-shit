from dataclasses import dataclass
from user.serializers import UserCreateSerializer

from .types import User


def create_new_user(request) -> User:
    """Создает нового пользователя."""

    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.create(serializer.validated_data)
    return User(**serializer.data)
