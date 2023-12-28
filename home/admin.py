from django.contrib import admin, messages
from .models import Product, ContactMessage, CustomDesign, Contact, User
from modeltranslation.admin import TranslationAdmin
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
from django.utils.html import strip_tags
from django.contrib.auth.admin import UserAdmin

@admin.register(Product)
class ProdructAdmin(TranslationAdmin):
    list_display = ('title',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(CustomDesign)
class CustomDesignAdmin(TranslationAdmin):
    list_display = ('title', 'description', 'additional_notes')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
        
    def save_model(self, request, obj, form, change):
        existing_records = Product.objects.exclude(pk=obj.pk).count()
        if existing_records >= 1:
            error_message = "Varat pievienot tikai divus ierakstus."
            self.message_user(request, error_message, level=messages.ERROR)
        else:
            super().save_model(request, obj, form, change)


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


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('address', 'postal_code', 'phone_number', 'email')

    fieldsets = (
        ('Kontaktinformācija', {
            'fields': ('address', 'postal_code', 'phone_number', 'email')
        }),
        ('Sociālie tīkli', {
            'fields': ('twitter_link', 'facebook_link', 'instagram_link'),
            'classes': ('collapse',),
        }),
    )

    class Meta:
        verbose_name = 'Kontaktinformācija'
        verbose_name_plural = 'Kontaktinformācija'

    def save_model(self, request, obj, form, change):
        existing_records = Contact.objects.exclude(pk=obj.pk).count()
        if existing_records >= 1:
            error_message = "Varat pievienot tikai divus ierakstus."
            self.message_user(request, error_message, level=messages.ERROR)
        else:
            super().save_model(request, obj, form, change)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        # Add any other custom fieldsets as needed
    )

    # Customize the list_display and list_filter attributes if necessary
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')

