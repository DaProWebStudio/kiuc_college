from modeltranslation.translator import register, TranslationOptions
from .models import InternationalCooperation


@register(InternationalCooperation)
class InternationalCooperationTranslation(TranslationOptions):
    fields = ('title', 'description',)
