from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.specialty.models import Specialty


@admin.register(Specialty)
class AdminSpecialty(TranslationAdmin):
    model = Specialty
    # prepopulated_fields = {'slug': ('title',)}



