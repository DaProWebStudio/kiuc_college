from django.contrib import admin
from django.utils.safestring import mark_safe

from modeltranslation.admin import TabbedTranslationAdmin

from apps.specialty.models import Specialty


@admin.register(Specialty)
class AdminSpecialty(TabbedTranslationAdmin):
    model = Specialty
    list_display = ('title', 'contract', 'form_of_training', 'get_photo')
    readonly_fields = ('get_photo',)
    exclude = ('slug',)

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="75">')

    get_photo.short_description = "Миниатюра"
