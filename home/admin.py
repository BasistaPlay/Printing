from django.contrib import admin, messages
from .models import Product, CustomUser, ContactMessage
from modeltranslation.admin import TranslationAdmin
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
from django.utils.html import strip_tags

@admin.register(Product)
class ProdructAdmin(TranslationAdmin):
    list_display = ('title', 'moto')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class ContactMessageAdminForm(forms.ModelForm):
    admin_message = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = ContactMessage
        fields = '__all__'

class ContactMessageAdmin(admin.ModelAdmin):
    form = ContactMessageAdminForm
    list_display = ('first_name', 'last_name', 'email', 'replied')
    list_filter = ('replied',)
    actions = ['mark_as_replied']

    def mark_as_replied(self, request, queryset):
        queryset.update(replied=True)

    mark_as_replied.short_description = 'Mark selected messages as replied'

    readonly_fields = ('first_name', 'last_name', 'email', 'phone_number', 'message','replied' )

    fieldsets = (
        ('User Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'message', 'replied'),
        }),
        ('Admin Info', {
            'fields': ('admin_subject', 'admin_message'),
        }),
    )

    def response_change(self, request, obj):
        if "_save" in request.POST:
            user_email = obj.email
            admin_subject = obj.admin_subject
            admin_message = obj.admin_message

            # Saglabājiet tikai attīrītu tekstu
            plain_text_admin_message = strip_tags(admin_message)

            subject_user = f"Atbilde uz jūsu jautājumu: {admin_subject}"

            # Izmantojiet HTML tagus kā tekstu, bet ziņojuma content_subtype iestatīšana uz HTML
            send_mail(
                subject_user,
                plain_text_admin_message,  # Izmantojiet attīrītu tekstu šeit
                settings.DEFAULT_FROM_EMAIL,
                [user_email],
                html_message=admin_message,  # Izmantojiet oriģinālo HTML ziņojumu šeit
                fail_silently=False,
            )

            obj.replied = True
            obj.save()

            messages.success(request, 'Atbilde nosūtīta lietotājam!')
            return super().response_change(request, obj)

        return super().response_change(request, obj)

# Piesakieties izmantot pārveidoto admin klasi
admin.site.register(ContactMessage, ContactMessageAdmin)