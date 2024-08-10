from django.contrib import admin
from stripe_integration.models import StripeKeys

@admin.register(StripeKeys)
class StripeKeysAdmin(admin.ModelAdmin):
    list_display = ('public_key', 'secret_key', 'endpoint_secret')
    search_fields = ('public_key', 'secret_key', 'endpoint_secret')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(pk__in=StripeKeys.objects.values_list('pk', flat=True)[:1])

    def save_model(self, request, obj, form, change):
        if StripeKeys.objects.exists() and not change:
            return
        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return not StripeKeys.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return StripeKeys.objects.exists()

    def has_change_permission(self, request, obj=None):
        return StripeKeys.objects.exists()