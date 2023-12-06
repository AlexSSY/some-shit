from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from user import  services


@api_view(['POST'])
def change_email_view(request):
    """Изменяет email текущего пользователя."""

    return Response(services.change_user_email(request), status=status.HTTP_200_OK)
