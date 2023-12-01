from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import (
    extend_schema, 
    OpenApiResponse, 
    OpenApiExample,
    OpenApiRequest,
    inline_serializer
)

from drf_standardized_errors.openapi_serializers import Error403Serializer

from rest_framework.decorators import (
    api_view, 
    permission_classes, 
    throttle_classes, 
    parser_classes,
    renderer_classes
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, parsers, renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from .serializers import UserRetrieve
from core.SchemaSerializers import AuthTokenRequestBody, AuthTokenResponse


@extend_schema(
        auth=(),
        description=_('Returns auth token for authenticate your requests'),
        request=AuthTokenRequestBody,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=AuthTokenResponse,
                description=_('Valid response'),
                examples=[
                    OpenApiExample(
                        name=_('Example'),
                        summary=_('Summary'),
                        description=_('Description'),
                        value={'token': 'fghdfjlkghglkj4g4lkg5ngkgfdgdfgfdg'},
                        response_only=True
                    )
                ]
            )
        }
)
@api_view(['POST'])
@permission_classes([])
@throttle_classes([])
@parser_classes([parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser])
@renderer_classes([renderers.JSONRenderer])
def get_auth_token(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})


@extend_schema(
        description=_('Logout current logged-in user'),
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description=_('Successful response')
            )
        }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def destroy_auth_token(request):
    user = request.user
    user_token = Token.objects.filter(user=user).last()
    if user_token:
        user_token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    description=_('Retrieve information about current logged-in user'),
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=UserRetrieve,
            description='Successful response',
            examples=[
                OpenApiExample(
                    name=_('Example'),
                    summary=_('Successful response'),
                    description=_('This value is valid returned data'),
                    value={
                        'id': 1,
                        'email': 'johndoe@mail.com',
                        'first_name': 'John',
                        'last_name': 'Doe',
                        'is_active': True
                    },
                    response_only=True
                )
            ]
        ),
        status.HTTP_403_FORBIDDEN: OpenApiResponse(
            response=Error403Serializer
        )
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    me = request.user
    serializer = UserRetrieve(me)
    serialized_data = serializer.data
    return Response(serialized_data, status.HTTP_200_OK)


def change_email(request):
    pass