from django.contrib import admin, messages
from django.conf import settings
from modeltranslation.admin import TranslationAdmin
from .models import CustomDesign
from django.utils.translation import gettext_lazy as _

@admin.register(CustomDesign)
class CustomDesignAdmin(TranslationAdmin):
    list_display = ('title', 'description', 'additional_notes')

    class Media:
        js = [
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',
            settings.STATIC_URL + 'modeltranslation/js/tabbed_translation_fields.js',
        ]
        css = {
            'all': (settings.STATIC_URL + 'modeltranslation/css/tabbed_translation_fields.css',),
        }
    def save_model(self, request, obj, form, change):
        existing_records = CustomDesign.objects.exclude(pk=obj.pk).count()
        if existing_records >= 1:
            error_message = _("Varat pievienot tikai vienu ierakstu.")
            self.message_user(request, error_message, level=messages.ERROR)
        else:
            super().save_model(request, obj, form, change)


# class PurchaseProductInline(admin.TabularInline):
#     model = PurchaseProduct
#     extra = 0
#     readonly_fields = ['product', 'quantity']

# class PurchaseAdmin(admin.ModelAdmin):
#     list_display = ('order_number', 'amount', 'user', 'status', 'created_at')
#     search_fields = ('order_number', 'user__username')
#     list_filter = ('status', 'created_at')
#     readonly_fields = ['order_number', 'amount', 'user', 'created_at']
#     inlines = [PurchaseProductInline]

# admin.site.register(Purchase, PurchaseAdmin)
