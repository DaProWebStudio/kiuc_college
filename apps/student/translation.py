from modeltranslation.translator import register, TranslationOptions
from .models import StudentLive


@register(StudentLive)
class StudentLiveTranslation(TranslationOptions):
    fields = ('title', 'description',)
