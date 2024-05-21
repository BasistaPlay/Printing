from django.contrib import admin, messages
from stripe_integration.models import StripeKeys
from django.utils.translation import gettext_lazy as _

@admin.register(StripeKeys)
class CustomDesignAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        existing_records = StripeKeys.objects.exclude(pk=obj.pk).count()
        if existing_records >= 1:
            error_message = _("Varat pievienot tikai vienu ierakstu.")
            self.message_user(request, error_message, level=messages.ERROR)
        else:
            super().save_model(request, obj, form, change)