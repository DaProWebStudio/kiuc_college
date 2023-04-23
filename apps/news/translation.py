from modeltranslation.translator import register, TranslationOptions
from .models import News


@register(News)
class NewsTranslation(TranslationOptions):
    fields = ('title', 'description',)
