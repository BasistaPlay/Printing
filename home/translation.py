from modeltranslation.translator import register, TranslationOptions

from .models import Product, CustomDesign, Category

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'options')

@register(CustomDesign)
class CustomDesignTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'additional_notes')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)
