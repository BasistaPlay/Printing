from django.contrib import admin, messages
from django.conf import settings
from django import forms
from django.core.mail import send_mail
from django.utils.html import format_html, strip_tags
from ckeditor.widgets import CKEditorWidget
from modeltranslation.admin import TranslationAdmin
from .models import (Product, ContactMessage, CustomDesign, Contact, Product_list,
                     Rating, user, GiftCode, Color, Size, TextList, ImageList, Order)
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('title',)

    fieldsets = (
        (_('Produkts'), {
            'fields': ('title', 'image', 'slug'),
        }),
        (_('Cena'), {
            'fields': ('price', 'options'),
        }),
        (_('Bildes'), {
            'fields': ('front_image_with_background', 'front_image_not_background', 'back_image_with_background', 'back_image_not_background'),
        }),
        (_('Krāsas'), {
            'fields': ('available_colors',),
        }),
        (_('Izmēri'), {
            'fields': ('available_sizes',),
        }),
    )

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name','code')

    fieldsets = (
        (_('Krāsas'), {
            'fields': ('name', 'code',),
        }),
    )

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name','size')

    fieldsets = (
        (_('Izmēri'), {
            'fields': ('name', 'size',),
        }),
    )

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
        existing_records = CustomDesign.objects.exclude(pk=obj.pk).count()
        if existing_records >= 1:
            error_message = _("Varat pievienot tikai vienu ierakstu.")
            self.message_user(request, error_message, level=messages.ERROR)
        else:
            super().save_model(request, obj, form, change)

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
            user_email = obj.email
            admin_subject = obj.admin_subject
            admin_message = obj.admin_message

            plain_text_admin_message = strip_tags(admin_message)

            subject_user = ("Response to your inquiry: {admin_subject}").format(admin_subject=admin_subject)

            send_mail(
                subject_user,
                plain_text_admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [user_email],
                html_message=admin_message,
                fail_silently=False,
            )

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

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1

@admin.register(Product_list)
class ProductListAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author', 'product', 'display_front_image')
    search_fields = ['title', 'author__username']
    inlines = [RatingInline]

    def display_front_image(self, obj):
        return format_html('<img src="{}" style="width:50px;height:50px;"/>', obj.front_image.url)

    display_front_image.short_description = _('Priekšējais attēls')

admin.site.register(GiftCode)

from django.contrib import admin
from django.utils.html import mark_safe
from .models import Order, ImageList, TextList

class TextListInline(admin.TabularInline):
    model = TextList
    readonly_fields = ['text', 'font', 'text_size', 'text_color']
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj):
        return False

from django.utils.safestring import mark_safe
from django.contrib import admin
from django.urls import reverse

import base64
class ImageListInline(admin.TabularInline):
    model = ImageList
    fields = ('image_preview', 'download_image')
    readonly_fields = ('image_preview', 'download_image')
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def image_preview(self, obj):
        return format_html('<img src="{url}" width="{width}" height="{height}" />', url=obj.image, width='auto', height='200px')
    image_preview.short_description = 'Preview'

    def download_image(self, obj):
        return format_html('<a href="{url}" download="front_image">Download PNG</a>', url=obj.image)
    download_image.short_description = 'Download front image'

    def has_change_permission(self, request, obj=None):
        return False

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'publish_product', 'allow_publish']
    readonly_fields = ['author', 'publish_product', 'back_image', 'product_color', 'product_amount', 'product_size', 'display_product_color', 'front_img', 'back_img', 'download_button_back', 'download_button_front']
    fieldsets = (
        (None, {
            'fields': ('author', 'publish_product', 'allow_publish')
        }),
        ('Product Information', {
            'fields': ('product_color','display_product_color', 'product_amount', 'product_size')
        }),
        ('Product Images', {
            'fields': ('front_img', 'download_button_front', 'back_img', 'download_button_back'), 
        }),
    )
    inlines = [TextListInline, ImageListInline]

    
    def front_img(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
            url=obj.front_image,
            width='auto',
            height='200px',
        ))
    
    def back_img(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" />'.format(
            url=obj.back_image,
            width='auto',
            height='200px',
        ))
    
    def download_button_front(self, obj):
        return format_html('<a href="{url}" download="front_image">Download PNG</a>', url=obj.front_image)
    download_button_front.short_description = 'Download front image'

    def download_button_back(self, obj):
        return format_html('<a href="{url}" download="front_image">Download PNG</a>', url=obj.back_image)
    download_button_back.short_description = 'Download back image'

    def display_product_color(self, obj):
        return format_html('<div style="width: 20px; height: 20px; background-color: {};"></div>', obj.product_color.code)
    display_product_color.short_description = 'Product Color'

    

admin.site.register(Order, OrderAdmin)