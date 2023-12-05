from rest_framework.throttling import UserRateThrottle


class SendEmailThrottle(UserRateThrottle):
    """Ограничение на один запрос в минуту"""

    scope = "send_email"
