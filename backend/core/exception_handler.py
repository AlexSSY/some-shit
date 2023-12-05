from drf_standardized_errors.handler import ExceptionHandler
from rest_framework.exceptions import APIException
import smtplib


class APISmtpDataError(APIException):
    status_code = 503
    default_detail = 'SMTP message rejected, please try again later.'
    default_code = 'smtp_message_rejected'


class MyExceptionHandler(ExceptionHandler):

    def convert_known_exceptions(self, exc: Exception) -> Exception:
        if isinstance(exc, smtplib.SMTPDataError):
            return APISmtpDataError()
        else:
            return super().convert_known_exceptions(exc)