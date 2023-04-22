from modeltranslation.translator import register, TranslationOptions
from .models import Specialty


@register(Specialty)
class SpecialtyTranslation(TranslationOptions):
    fields = ('title', 'description')
