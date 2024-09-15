from modeltranslation.translator import register, TranslationOptions

from home.models import CustomDesign
from Product.models import Product
from Product.models import Category
from User_app.models import FAQ


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'options')

@register(CustomDesign)
class CustomDesignTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'additional_notes')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')
