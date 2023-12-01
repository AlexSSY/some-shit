from django.urls import path
from .views import get_me


urlpatterns = [
    path('me', get_me),
]
