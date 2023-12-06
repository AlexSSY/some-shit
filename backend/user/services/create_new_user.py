from dataclasses import dataclass
from user.serializers import UserCreateSerializer

from .types import UserDict


def create_new_user(request) -> UserDict:
    """Создает нового пользователя."""

    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.create(serializer.validated_data)
    return UserDict(**serializer.data)
