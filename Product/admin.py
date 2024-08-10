from django.contrib import admin
from django.conf import settings
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from .models import (Product, Rating, Category)
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import mark_safe

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


# from django_recaptcha.models import RecaptchaKeys

# class RecaptchaKeysAdmin(admin.ModelAdmin):
#     list_display = ('public_key', 'private_key')
#     search_fields = ['public_key', 'private_key']

#     def save_model(self, request, obj, form, change):
#         existing_records = RecaptchaKeys.objects.exclude(pk=obj.pk).count()
#         if existing_records >= 1:
#             error_message = _("Varat pievienot tikai vienu ierakstu.")
#             self.message_user(request, error_message, level=messages.ERROR)
#         else:
#             super().save_model(request, obj, form, change)

# admin.site.register(RecaptchaKeys, RecaptchaKeysAdmin)