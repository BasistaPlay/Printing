from django.contrib import admin, messages
from django.conf import settings
from django import forms
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.html import format_html, strip_tags
from ckeditor.widgets import CKEditorWidget
from modeltranslation.admin import TranslationAdmin
from .models import (Product, CustomDesign,
                    Rating, GiftCode, Color, Size, TextList, ImageList, Order, Purchase, Category)
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import mark_safe
from django.template.loader import render_to_string

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('title',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title_en',)}

    fieldsets = (
        (_('General'), {
            'fields': ('title', 'slug', 'image'),
        }),
    )

    def image_thumbnail(self, obj):
        if obj.image:
            return '<img src="%s" style="max-height: 100px; max-width: 150px;" />' % obj.image.url
        else:
            return _('No Image')

    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = _('Thumbnail')

    class Media:
        js = [
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',  # Jaunāka jQuery versija
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',  # Jaunāka jQuery UI versija
            settings.STATIC_URL + 'modeltranslation/js/tabbed_translation_fields.js',  # Lokāli glabāts JS fails
        ]
        css = {
            'all': (settings.STATIC_URL + 'modeltranslation/css/tabbed_translation_fields.css',),  # Lokāli glabāts CSS fails
        }


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('title',)

    fieldsets = (
        (_('Produkts'), {
            'fields': ('title', 'categories', 'image', 'slug', 'views'),
        }),
        (_('Cena'), {
            'fields': ('price', 'options'),
        }),
        (_('Bildes'), {
            'fields': ('front_image_with_background', 'front_image_not_background', 'back_image_with_background', 'back_image_not_background', 'front_image_coords', 'back_image_coords'),
        }),
        (_('Krāsas'), {
            'fields': ('available_colors',),
        }),
        (_('Izmēri'), {
            'fields': ('available_sizes',),
        }),
    )

    readonly_fields = ('views', )


    class Media:
        js = [
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',  # Jaunāka jQuery versija
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',  # Jaunāka jQuery UI versija
            settings.STATIC_URL + 'modeltranslation/js/tabbed_translation_fields.js',  # Lokāli glabāts JS fails
        ]
        css = {
            'all': (settings.STATIC_URL + 'modeltranslation/css/tabbed_translation_fields.css',),  # Lokāli glabāts CSS fails
        }
        
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
            'https://cdnjs.cloudflare.com/ajax/libs/fabric.js/4.5.0/fabric.min.js',
            'js/custom_admin.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
            'all': ('css/custom_admin.css',)
        }

    def save_model(self, request, obj, form, change):
        # Ensure front_image_coords and back_image_coords are saved properly
        if 'front_image_coords' in form.cleaned_data:
            obj.front_image_coords = form.cleaned_data['front_image_coords']
        if 'back_image_coords' in form.cleaned_data:
            obj.back_image_coords = form.cleaned_data['back_image_coords']

        super().save_model(request, obj, form, change)

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
        js = [
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',  # Jaunāka jQuery versija
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js',  # Jaunāka jQuery UI versija
            settings.STATIC_URL + 'modeltranslation/js/tabbed_translation_fields.js',  # Lokāli glabāts JS fails
        ]
        css = {
            'all': (settings.STATIC_URL + 'modeltranslation/css/tabbed_translation_fields.css',),  # Lokāli glabāts CSS fails
        }

    def save_model(self, request, obj, form, change):
        existing_records = CustomDesign.objects.exclude(pk=obj.pk).count()
        if existing_records >= 1:
            error_message = _("Varat pievienot tikai vienu ierakstu.")
            self.message_user(request, error_message, level=messages.ERROR)
        else:
            super().save_model(request, obj, form, change)

# class ContactMessageAdminForm(forms.ModelForm):
#     admin_message = forms.CharField(widget=CKEditorWidget())
#     class Meta:
#         model = ContactMessage
#         fields = '__all__'

# @admin.register(ContactMessage)
# class ContactMessageAdmin(admin.ModelAdmin):
#     form = ContactMessageAdminForm
#     list_display = ('first_name', 'last_name', 'email', 'replied')
#     list_filter = ('replied',)
#     actions = ['mark_as_replied']

#     def mark_as_replied(self, request, queryset):
#         queryset.update(replied=True)

#     mark_as_replied.short_description = _('Atzīmēt atlasītās ziņas kā atbildētas')

#     readonly_fields = ('first_name', 'last_name', 'email', 'phone_number', 'message','replied' )

#     fieldsets = (
#         (_('Lietotāja informācija'), {
#             'fields': ('first_name', 'last_name', 'email', 'phone_number', 'message', 'replied'),
#         }),
#         (_('Administratora ziņojums'), {
#             'fields': ('admin_subject', 'admin_message'),
#         }),
#     )

#     def response_change(self, request, obj):
#         if "_save" in request.POST:
#             user_email = [obj.email]  # pārliecināsimies, ka user_email ir saraksts
#             admin_subject = obj.admin_subject
#             admin_message = obj.admin_message

#             html_content = render_to_string('e-mail/answer_message.html', {'admin_message': admin_message})

#             subject_user = f"Atbilde uz jūsu jautājumu: {admin_subject}"
#             email = EmailMultiAlternatives(subject_user, strip_tags(admin_message), settings.DEFAULT_FROM_EMAIL, user_email)
#             email.attach_alternative(html_content, "text/html")
#             email.send()

#             obj.replied = True
#             obj.save()

#             messages.success(request, _('Atbilde nosūtīta lietotājam!'))
#             return super().response_change(request, obj)

#         return super().response_change(request, obj)


# @admin.register(Contact)
# class ContactAdmin(admin.ModelAdmin):
#     list_display = ('address', 'postal_code', 'phone_number', 'email')

#     fieldsets = (
#         (_('Kontaktinformācija'), {
#             'fields': ('address', 'postal_code', 'phone_number', 'email')
#         }),
#         (_('Sociālās saites'), {
#             'fields': ('twitter_link', 'facebook_link', 'instagram_link'),
#             'classes': ('collapse',),
#         }),
#     )

#     def save_model(self, request, obj, form, change):
#         existing_records = Contact.objects.exclude(pk=obj.pk).count()
#         if existing_records >= 1:
#             error_message = _("You can only add one record.")
#             self.message_user(request, error_message, level=messages.ERROR)
#         else:
#             super().save_model(request, obj, form, change)

# @admin.register(user)
# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         (_('Personiskā informācija'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
#         (_('Atļaujas'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         (_('Svarīgie datumi'), {'fields': ('last_login', 'date_joined')}),
#     )

#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
#     list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')

#     class Media:
#         js = (
#             'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
#             'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
#             'modeltranslation/js/tabbed_translation_fields.js',
#         )
#         css = {
#             'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
#         }

class RatingInline(admin.TabularInline):
    readonly_fields = ['user', 'stars']
    can_delete = False
    extra = 0
    model = Rating

    def has_add_permission(self, request, obj):
        return False


    def image_preview(self, obj):
        return format_html('<img src="{url}" width="{width}" height="{height}" />', url=obj.front_image, width='auto', height='100px')
    image_preview.short_description = 'Preview'

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

    def display_product_color(self, obj):
        return format_html('<div style="width: 20px; height: 20px; background-color: {};"></div>', obj.product_color.code)
    display_product_color.short_description = 'Product Color'

admin.site.register(GiftCode)

class TextListInline(admin.TabularInline):
    model = TextList
    readonly_fields = ['text', 'font', 'text_size','text_color', 'display_text_color']
    can_delete = False
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def display_text_color(self, obj):
        return format_html('<div style="border: 1px solid black; width: 20px; height: 20px; background-color: {};"></div>', obj.text_color)
    display_text_color.short_description = 'Text Color'


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
    list_display = ['id', 'product', 'author', 'publish_product', 'allow_publish', 'average_rating']
    readonly_fields = ['product', 'author', 'publish_product', 'back_image', 'product_color', 'display_product_color', 'average_rating', 'display_front_image', 'display_back_image', 'download_button_front', 'download_button_back']
    search_fields = ['author__username', 'id']
    list_filter = ['product', 'publish_product']
    fieldsets = (
        (None, {
            'fields': ('product', 'author', 'publish_product', 'allow_publish')
        }),
        ('Product Information', {
            'fields': ('title', 'description', 'product_color', 'display_product_color', 'average_rating')
        }),
        ('Product Images', {
            'fields': ('display_front_image','download_button_front', 'display_back_image', 'download_button_back'),
        }),
    )
    inlines = [TextListInline, ImageListInline, RatingInline]

    def display_front_image(self, obj):
        if obj.front_image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />'.format(obj.front_image.url))
        else:
            return "-"
    display_front_image.short_description = 'Front Image'

    def display_back_image(self, obj):
        if obj.back_image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />'.format(obj.back_image.url))
        else:
            return "-"
    display_back_image.short_description = 'Back Image'

    def download_button_front(self, obj):
        if obj.front_image:
            return format_html('<a href="{0}" download="{1}_front.png">Download PNG</a>', obj.front_image.url, obj.product.slug)
        else:
            return "-"
    download_button_front.short_description = 'Download front image'

    def download_button_back(self, obj):
        if obj.back_image:
            return format_html('<a href="{0}" download="{1}_back.png">Download PNG</a>', obj.back_image.url, obj.product.slug)
        else:
            return "-"
    download_button_back.short_description = 'Download back image'

    def display_product_color(self, obj):
        return format_html('<div style="width: 20px; height: 20px; background-color: {};"></div>', obj.product_color.code)
    display_product_color.short_description = 'Product Color'

from django_recaptcha.models import RecaptchaKeys

class RecaptchaKeysAdmin(admin.ModelAdmin):
    list_display = ('public_key', 'private_key')
    search_fields = ['public_key', 'private_key']

    def save_model(self, request, obj, form, change):
        existing_records = RecaptchaKeys.objects.exclude(pk=obj.pk).count()
        if existing_records >= 1:
            error_message = _("Varat pievienot tikai vienu ierakstu.")
            self.message_user(request, error_message, level=messages.ERROR)
        else:
            super().save_model(request, obj, form, change)

admin.site.register(RecaptchaKeys, RecaptchaKeysAdmin)


admin.site.register(Order, OrderAdmin)

from django.contrib import admin
from .models import Purchase, PurchaseProduct

class PurchaseProductInline(admin.TabularInline):  # Inline tabula produktiem pasūtījumā
    model = PurchaseProduct
    extra = 0
    readonly_fields = ['product', 'quantity']

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'amount', 'user', 'status', 'created_at')
    search_fields = ('order_number', 'user__username')
    list_filter = ('status', 'created_at')
    readonly_fields = ['order_number', 'amount', 'user', 'created_at']
    inlines = [PurchaseProductInline]

admin.site.register(Purchase, PurchaseAdmin)
