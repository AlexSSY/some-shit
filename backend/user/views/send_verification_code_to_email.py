from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view, throttle_classes
from rest_framework import status
from rest_framework.response import Response

from user import throttling, services


@api_view(["POST"])
@throttle_classes([throttling.SendEmailThrottle])
def send_verification_code_to_email_view(request):
    """Отправляет код для верификации по email текущему пользователю."""

    services.send_verification_code_to_email(request)
    return Response(status=status.HTTP_204_NO_CONTENT)
