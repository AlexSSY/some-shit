from rest_framework import serializers
from .models import User


class UserRetrieve(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_active')
        read_only_fields = ('id', 'email', 'first_name', 'last_name', 'is_active')
