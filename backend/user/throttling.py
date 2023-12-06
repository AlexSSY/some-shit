from rest_framework.throttling import UserRateThrottle


class SendEmailThrottle(UserRateThrottle):
    """Ограничение количества запросов."""

    scope = "send_email"
