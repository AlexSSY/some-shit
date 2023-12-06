from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from user.settings import settings
from user.models import ConfirmationCode
from user.serializers import SendCodeToEmailSerializer


def send_verification_code_to_email(request) -> None:
    """Отправляет код на email (Запрос должен быть авторизованным)."""

    to_email = _get_email_from_request_body(request)

    verification = ConfirmationCode.objects.create(email=to_email)
    
    mail_subject = _('Activate your account.')
    message = _get_email_message_text(verification.code)
    send_mail(mail_subject, message, html_message=message, 
              from_email=settings.EMAIL_HOST_USER, recipient_list=[to_email])


def _get_email_from_request_body(request) -> str:
    """Возвращает email если он был передан клиентом, 
    в противном случае возвращает email текущего пользователя."""

    serializer = SendCodeToEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data.get("email", request.user.email)


def _get_email_message_text(verification_code: str) -> str:
    """Возвращает текст сообщения"""

    return render_to_string(template_name='verification_email.html', 
        context={'code': verification_code})
