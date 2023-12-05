from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ConfirmationCode
from . import services


@admin.register(ConfirmationCode)
class ConfirmationCodeAdmin(admin.ModelAdmin):
    """Админка для ConfirmationCode"""

    list_display = ('code', 'email', "_is_fresh")
    fields = ("email", 'code', 'created_at', '_is_fresh')
    readonly_fields = ('created_at', "_is_fresh")

    @admin.display(description=_("Is Fresh"), boolean=True)
    def _is_fresh(self, obj) -> bool:
        """Возвращает значение True если 
        время действия кода истекло"""

        return not services.is_code_expired(obj)
