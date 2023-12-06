from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import status, parsers
from rest_framework.response import Response

from user import  services


@api_view(['POST'])
@permission_classes([])
@parser_classes([parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser])
def create_new_user_view(request):
    """Создание нового пользователя."""

    return Response(data=services.create_new_user(request), status=status.HTTP_201_CREATED)
