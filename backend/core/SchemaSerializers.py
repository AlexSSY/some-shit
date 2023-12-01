from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


class ErrorDetailSerializer(serializers.Serializer):
    detail = serializers.CharField()


@extend_schema_serializer(
    many=False,
    examples=[
        OpenApiExample(
            name=_('Example'),
            summary=_('Summary'),
            description=_('Description'),
            value={
                'username': 'username@mail.com',
                'password': 'some-password'
            },
            request_only=True
        )
    ]
)
class AuthTokenRequestBody(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AuthTokenResponse(serializers.Serializer):
    token = serializers.CharField()
