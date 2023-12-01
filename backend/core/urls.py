from django.contrib import admin
from django.urls import path, include
from user.urls import urlpatterns as user_urls

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.authtoken import views as token_auth_views

urlpatterns = [
    path('api-token-auth/', token_auth_views.obtain_auth_token),
    path('admin/', admin.site.urls),
    path('api/v1/user/', include(user_urls)),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
