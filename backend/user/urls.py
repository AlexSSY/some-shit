from django.urls import path
from .views import get_user

urlpatterns = [
    path('<int:pk>', get_user),
]
