from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from rest_framework import exceptions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token as AuthToken
from datetime import timedelta
from enum import Enum

from .serializers import UserCreateSerializer, ConfirmationCodeSerializer, \
    ConfirmationCodeAndEmailSerializer, UserRetrieveSerializer, SendCodeToEmailSerializer
from .models import ConfirmationCode
from .settings import settings

def send_verification_code_to_email(request) -> None:
    """Отправляет код на email (Запрос должен быть авторизованным)."""

    serializer = SendCodeToEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    to_email = serializer.validated_data.get("email", request.user.email)

    verification = ConfirmationCode.objects.create(email=to_email)
    mail_subject = _('Activate your account.')
    message = render_to_string(template_name='verification_email.html', 
        context={'code': verification.code})
    send_mail(mail_subject, message, html_message=message, 
              from_email=settings.EMAIL_HOST_USER, recipient_list=[to_email])


def is_code_expired(confirmation_code: ConfirmationCode) -> bool:
    """Возвращает True если срок действия кода истек"""

    lifetime = timedelta(minutes=settings.CONFIRM_CODE_LIFETIME_IN_MINUTES)
    return (timezone.now() - confirmation_code.created_at) >= lifetime


CodeStatus = Enum("CodeStatus", ("VALID", "NOT_FOUND", "EXPIRED"))


def _get_code_status(email: str, code: str) -> CodeStatus:
    """Возвращает CodeStatus.VALID если по указанному email 
    существует код **code**, и он не expired"""

    queryset = ConfirmationCode.objects.filter(email=email, code=code)
    confirmation_code = queryset.first()
    if confirmation_code is None:
        return CodeStatus.NOT_FOUND
    if is_code_expired(confirmation_code):
        return CodeStatus.EXPIRED
    return CodeStatus.VALID


def create_new_user(request) -> dict:
    """Создает нового пользователя."""

    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.create(serializer.validated_data)
    return serializer.data


def verify_new_user_email(request) -> None:
    """Верифицирует email текущего пользователя."""

    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = request.user.email
    code = serializer.validated_data["code"]
    _verify_email_code(email, code)
    request.user.email_verified = True
    request.user.save()
    

def change_user_email(request) -> dict:
    """Изменяет email пользователя"""

    serializer = ConfirmationCodeAndEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]
    code = serializer.validated_data["code"]
    _verify_email_code(email, code)
    request.user.email = email
    request.user.email_verified = True
    request.user.save()
    return UserRetrieveSerializer(instance=request.user).data


def _verify_email_code(email: str, code: str) -> None:
    """Не выдаст исключения если верификация успешна."""

    code_status = _get_code_status(email=email, code=code)
    if code_status == CodeStatus.NOT_FOUND:
        raise exceptions.NotAuthenticated(detail="code not exists", code="code_not_exists")
    if code_status == CodeStatus.EXPIRED:
        raise exceptions.NotAuthenticated(detail="code expired", code="code_expired")
    

def get_me(request) -> dict:
    """Возвращает словарь с информацией о текущем пользователе."""

    return UserRetrieveSerializer(request.user).data


def get_auth_token(request) -> str:
    """Возвращает токен для авторизации запросов."""

    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, is_created = AuthToken.objects.get_or_create(user=user)
    user.last_login = timezone.now()
    user.save()
    return token.key


def destroy_auth_token(request) -> None:
    """Уничтожает токен если такой существует"""

    user = request.user
    user_token = AuthToken.objects.filter(user=user).last()
    if user_token:
        user_token.delete()
