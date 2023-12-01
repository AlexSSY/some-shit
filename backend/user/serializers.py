from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from .models import User


class UserRetrieve(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active')
        read_only_fields = ('id', 'email', 'first_name', 'last_name', 'is_active')


@extend_schema_serializer(
    many=False,
    examples=[
        OpenApiExample(
            name=_('Example'),
            summary=_('Valid request'),
            description=_('Valid request body example'),
            value={
                'email': 'johndoe@mail.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'password',
                'password1': 'password',
            }
        )
    ]
)
class UserCreate(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise ValidationError(detail=_('password confirmation error'))
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('password')
        validated_data.pop('password1')
        return super().create(validated_data)

    class Meta:
        model = User
        fields = (
            'id', 
            'email', 
            'first_name', 
            'last_name', 
            'is_active', 
            'password', 
            'password1'
        )
        read_only_fields = (
            'id', 
            'is_active',
            'password',
            'password1'
        )
