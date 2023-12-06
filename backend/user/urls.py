from django.urls import path
from . import views


urlpatterns = [
    path('myself', views.get_current_user_view),
    path('create/', views.create_new_user_view),
    path('send-code/', views.send_verification_code_to_email_view),
    path('verify-email/', views.verify_new_user_email_view),
    path('token-get/', views.get_auth_token_view),
    path('token-destroy', views.destroy_auth_token_view)
]
