from user.serializers import ConfirmationCodeAndEmailSerializer, \
    UserRetrieveSerializer

from .verify_new_user_email import verify_email_code
from .types import User


def change_user_email(request) -> User:
    """Изменяет email пользователя"""

    serializer = ConfirmationCodeAndEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]
    code = serializer.validated_data["code"]
    verify_email_code(email, code)
    request.user.email = email
    request.user.email_verified = True
    request.user.save()
    return User(**UserRetrieveSerializer(instance=request.user).data)
