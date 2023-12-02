from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from drf_spectacular.utils import (
    extend_schema, 
    OpenApiResponse, 
    OpenApiExample,
    OpenApiParameter
)
from drf_spectacular.types import OpenApiTypes

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
from rest_framework import exceptions

from .serializers import UserRetrieve, UserCreate
from .models import User, EmailVerification
from .decorators import email_verified
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
    user: User = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    user.last_login = timezone.now()
    user.save()
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
@email_verified
def get_me(request):
    me = request.user
    serializer = UserRetrieve(me)
    serialized_data = serializer.data
    return Response(serialized_data, status.HTTP_200_OK)


@extend_schema(
        auth=(),
        description=_('Create new unique user'),
        request=UserCreate,
        responses={
            status.HTTP_201_CREATED: UserRetrieve
        }
)
@api_view(['POST'])
@permission_classes([])
@parser_classes([parsers.JSONParser, parsers.FormParser, parsers.MultiPartParser])
def create(request):
    user_create_serializer = UserCreate(data=request.data)
    user_create_serializer.is_valid(raise_exception=True)
    validated_data = user_create_serializer.validated_data
    new_user = user_create_serializer.create(validated_data)
    user_retrieve_serializer = UserRetrieve(new_user)
    returned_data = user_retrieve_serializer.data
    return Response(data=returned_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def send_email_verification(request):
    verification, created = EmailVerification.objects.get_or_create(user=request.user)
    current_site = get_current_site(request)
    mail_subject = _('Activate your account.')
    message = render_to_string('verification_email.html', {
                'user': request.user,
                'domain': current_site.domain,
                'token': verification.token,
            })
    to_email = request.user.email
    send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
    return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
        auth=(),
        description=_('Email activation'),
        parameters=[
            OpenApiParameter(
                name='token', 
                type=OpenApiTypes.STR, 
                description=_('Activation token')
            )
        ]
)
@api_view(['GET'])
@permission_classes([])
def email_activate(request, token):
    email_verification = EmailVerification.objects.filter(token=token).first()
    if not email_verification:
        raise exceptions.AuthenticationFailed(detail=_('invalid activation token'))
    email_verification.user.email_verified = True
    email_verification.user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
