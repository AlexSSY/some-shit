from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from user import services


@api_view(['GET'])
def destroy_auth_token_view(request):
    """Уничтожает токен текущего пользователя."""

    services.destroy_auth_token(request)
    return Response(status=status.HTTP_204_NO_CONTENT)
