from modeltranslation.translator import register, TranslationOptions

from .models import Product, CustomDesign

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(CustomDesign)
class CustomDesignTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'additional_notes')
