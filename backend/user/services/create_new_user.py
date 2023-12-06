from dataclasses import dataclass
from user.serializers import UserCreateSerializer


def create_new_user(request) -> dict:
    """Создает нового пользователя."""

    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.create(serializer.validated_data)
    return serializer.data
