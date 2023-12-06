from rest_framework.authtoken.models import Token as AuthToken


def destroy_auth_token(request) -> None:
    """Уничтожает токен если такой существует."""

    AuthToken.objects.filter(user=request.user).last().delete()
