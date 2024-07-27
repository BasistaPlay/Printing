from django.contrib import admin
from django.contrib import admin, messages
from django.conf import settings
from django import forms
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from ckeditor.widgets import CKEditorWidget
from User_app.models import ContactMessage, Contact, user, EmailVerification
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import mark_safe
from django.template.loader import render_to_string


class ContactMessageAdminForm(forms.ModelForm):
    admin_message = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = ContactMessage
        fields = '__all__'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    form = ContactMessageAdminForm
    list_display = ('first_name', 'last_name', 'email', 'replied')
    list_filter = ('replied',)
    actions = ['mark_as_replied']

    def mark_as_replied(self, request, queryset):
        queryset.update(replied=True)

    mark_as_replied.short_description = _('Atzīmēt atlasītās ziņas kā atbildētas')

    readonly_fields = ('first_name', 'last_name', 'email', 'phone_number', 'message','replied' )

    fieldsets = (
        (_('Lietotāja informācija'), {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'message', 'replied'),
        }),
        (_('Administratora ziņojums'), {
            'fields': ('admin_subject', 'admin_message'),
        }),
    )

    def response_change(self, request, obj):
        if "_save" in request.POST:
            user_email = [obj.email]
            admin_subject = obj.admin_subject
            admin_message = obj.admin_message

            html_content = render_to_string('e-mail/answer_message.html', {'admin_message': admin_message})

            subject_user = f"Atbilde uz jūsu jautājumu: {admin_subject}"
            email = EmailMultiAlternatives(subject_user, strip_tags(admin_message), settings.DEFAULT_FROM_EMAIL, user_email)
            email.attach_alternative(html_content, "text/html")
            email.send()

            obj.replied = True
            obj.save()

            messages.success(request, _('Atbilde nosūtīta lietotājam!'))
            return super().response_change(request, obj)

        return super().response_change(request, obj)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('address', 'postal_code', 'phone_number', 'email')

    fieldsets = (
        (_('Kontaktinformācija'), {
            'fields': ('address', 'postal_code', 'phone_number', 'email')
        }),
        (_('Sociālās saites'), {
            'fields': ('twitter_link', 'facebook_link', 'instagram_link'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        existing_records = Contact.objects.exclude(pk=obj.pk).count()
        if existing_records >= 1:
            error_message = _("You can only add one record.")
            self.message_user(request, error_message, level=messages.ERROR)
        else:
            super().save_model(request, obj, form, change)

@admin.register(user)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personiskā informācija'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('Atļaujas'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Svarīgie datumi'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_code', 'created_at', 'is_verified')
    list_filter = ('is_verified',)

    readonly_fields = ('user', 'verification_code', 'created_at', 'is_verified')

    fieldsets = (
        (_('Lietotājs'), {
            'fields': ('user', 'verification_code', 'created_at', 'is_verified'),
        }),
    )

    # def has_add_permission(self, request):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return False