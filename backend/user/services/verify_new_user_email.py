from enum import Enum
from datetime import timedelta
from django.utils import timezone
from rest_framework import exceptions

from user.serializers import ConfirmationCodeSerializer
from user.models import ConfirmationCode
from user.settings import settings


def verify_new_user_email(request) -> None:
    """Верифицирует email текущего пользователя."""

    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = request.user.email
    code = serializer.validated_data["code"]
    verify_email_code(email, code)
    request.user.email_verified = True
    request.user.save()


def verify_email_code(email: str, code: str) -> None:
    """Не выдаст исключения если верификация успешна."""

    code_status = _get_code_status(email=email, code=code)
    if code_status == CodeStatus.NOT_FOUND:
        raise exceptions.NotAuthenticated(detail="code not exists", code="code_not_exists")
    if code_status == CodeStatus.EXPIRED:
        raise exceptions.NotAuthenticated(detail="code expired", code="code_expired")
    

CodeStatus = Enum("CodeStatus", ("VALID", "NOT_FOUND", "EXPIRED"))


def _get_code_status(email: str, code: str) -> CodeStatus:
    """Возвращает CodeStatus.VALID если по указанному email 
    существует код **code**, и он не expired"""

    queryset = ConfirmationCode.objects.filter(email=email, code=code)
    confirmation_code = queryset.first()

    if confirmation_code is None:
        return CodeStatus.NOT_FOUND
    if is_verification_code_expired(confirmation_code):
        return CodeStatus.EXPIRED
    
    return CodeStatus.VALID


def is_verification_code_expired(confirmation_code: ConfirmationCode) -> bool:
    """Возвращает True если срок действия кода истек"""

    lifetime = timedelta(minutes=settings.CONFIRM_CODE_LIFETIME_IN_MINUTES)
    return (timezone.now() - confirmation_code.created_at) >= lifetime
