from modeltranslation.translator import register, TranslationOptions
from .models import SaeJeon


@register(SaeJeon)
class SaeJeonTranslation(TranslationOptions):
    fields = ('title', 'description',)
