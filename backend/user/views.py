from django.utils.translation import gettext_lazy as _

from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from drf_standardized_errors.openapi_serializers import Error403Serializer

from rest_framework.decorators import (
    api_view, 
    permission_classes, 
    throttle_classes, 
    parser_classes
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserRetrieve


@api_view(['POST'])
@permission_classes([])
def get_auth_token(request):
    pass


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
