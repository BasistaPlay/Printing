from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import mark_safe
from design.models import Designs, TextList, ImageList
from Product.models import Rating

# Register your models here.


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

class DesignsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'author', 'publish_product', 'allow_publish', 'average_rating']
    readonly_fields = ['product', 'author', 'publish_product', 'back_image', 'product_color', 'display_product_color', 'average_rating', 'display_front_image', 'display_back_image', 'download_button_front', 'download_button_back', 'created_at']
    search_fields = ['author__username', 'id']
    list_filter = ['product', 'publish_product']
    fieldsets = (
        (None, {
            'fields': ('product', 'author', 'publish_product', 'allow_publish', 'created_at')
        }),
        ('Product Information', {
            'fields': ('title', 'product_color', 'display_product_color', 'average_rating')
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



admin.site.register(Designs, DesignsAdmin)