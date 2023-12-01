from django.utils.translation import gettext_lazy as _

from rest_framework import serializers


class ErrorDetailSerializer(serializers.Serializer):
    detail = serializers.CharField()
