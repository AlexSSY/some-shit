from django.conf import settings


settings.CONFIRM_CODE_LIFETIME_IN_MINUTES: int = getattr(settings, 'CONFIRM_CODE_LIFETIME_IN_MINUTES', 5)
