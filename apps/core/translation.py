from modeltranslation.translator import register, TranslationOptions
from .models import InternationalCooperation, ReceptionPage


@register(InternationalCooperation)
class InternationalCooperationTranslation(TranslationOptions):
    fields = ('title', 'description',)


@register(ReceptionPage)
class ReceptionPageTranslation(TranslationOptions):
    fields = ('heading', 'lead', 'body', 'contacts_title')
