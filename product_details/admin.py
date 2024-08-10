from django.contrib import admin
from product_details.models import Color, Size
from django.utils.translation import gettext as _


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