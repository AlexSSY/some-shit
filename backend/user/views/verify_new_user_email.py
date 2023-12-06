from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from user import services


@api_view(["POST"])
def verify_new_user_email_view(request):
    """Верификация email нового пользователя."""

    services.verify_new_user_email(request)
    return Response(status.HTTP_204_NO_CONTENT)
