from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view, permission_classes, parser_classes, \
    throttle_classes, renderer_classes
from rest_framework import status, parsers, renderers
from rest_framework.response import Response

from . import throttling, services


@api_view(['GET'])
def get_me_view(request):
    """Информация о текущем пользователе."""

    return Response(services.get_me(request))


@api_view(['POST'])
@permission_classes([])
@parser_classes([parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser])
def create(request):
    """Создание нового пользователя."""

    return Response(data=services.create_new_user(request), status=status.HTTP_201_CREATED)


@api_view(['POST'])
def change_email(request):
    """Изменяет email текущего пользователя."""

    return Response(services.change_user_email(request), status=status.HTTP_200_OK)


@api_view(["POST"])
@throttle_classes([throttling.SendEmailThrottle])
def send_verification_code_to_email_view(request):
    """Отправляет код для верификации по email текущему пользователю."""

    services.send_verification_code_to_email(request)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def verify_new_user_email_view(request):
    """Верификация email нового пользователя."""

    services.verify_new_user_email(request)
    return Response(status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([])
@throttle_classes([])
@parser_classes([parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser])
@renderer_classes([renderers.JSONRenderer])
def get_auth_token_view(request):
    """Получить токен для авторизации запросов на сервер."""

    return Response(data={"token": services.get_auth_token(request)}, 
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def destroy_auth_token_view(request):
    """Уничтожает токен текущего пользователя."""

    services.destroy_auth_token(request)
    return Response(status=status.HTTP_204_NO_CONTENT)
