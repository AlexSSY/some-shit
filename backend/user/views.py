from django.utils.translation import gettext as _
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from .serializers import UserRetrieve
from .models import User


@api_view(['GET'])
def get_user(request, pk: int):
    user: User = User.objects.filter(pk=pk).last()
    if not user:
        raise NotFound(detail=_('User with pk: %(pk)s not found') % {'pk': pk}, code=1)
    serializer = UserRetrieve(user)
    serialized_data = serializer.data
    return Response(serialized_data, status.HTTP_200_OK)
