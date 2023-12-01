from django.urls import path
from .views import get_me, create


urlpatterns = [
    path('me', get_me),
    path('create/', create)
]
