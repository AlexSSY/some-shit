from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from user import services
from user import serializers


@extend_schema(
        description="Retrieve information about current **logged-in** User",
        tags=('User',  ),
        responses={
            200: OpenApiResponse(
                response=serializers.UserRetrieveSerializer,
                description=_("Successful"),
                examples=[
                    OpenApiExample(
                        name=_("Successful"),
                        media_type="application/json",
                        summary=_("Successful"),
                        value={
                            "id": 228,
                            "email": "bob3@mail.ru",
                            "first_name": "Bob",
                            "last_name": "Marley",
                            "is_active": True,
                            "email_verified": True
                        },
                        response_only=True,
                        description=_("Successful response")
                    )
                ]
            )
        }
)
@api_view(['GET'])
def get_current_user_view(request):
    """Информация о текущем пользователе."""

    return Response(services.get_current_user(request))
