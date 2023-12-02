from django.urls import path
from .views import (
    get_me, 
    create,
    send_email_verification,
    email_activate
)


urlpatterns = [
    path('me', get_me),
    path('create/', create),
    path('email/verify/', send_email_verification),
    path('email/confirm/<str:token>', email_activate, name='activate')
]
