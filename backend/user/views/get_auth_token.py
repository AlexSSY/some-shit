from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view, permission_classes, parser_classes, \
    throttle_classes, renderer_classes
from rest_framework import status, parsers, renderers
from rest_framework.response import Response

from user import services


@api_view(['POST'])
@permission_classes([])
@throttle_classes([])
@parser_classes([parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser])
@renderer_classes([renderers.JSONRenderer])
def get_auth_token_view(request):
    """Получить токен для авторизации запросов на сервер."""

    return Response(data={"token": services.get_auth_token(request)}, 
                    status=status.HTTP_200_OK)
