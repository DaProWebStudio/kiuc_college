from django.contrib import admin

from modeltranslation.admin import TabbedTranslationAdmin


from apps.specialty.models import Specialty


@admin.register(Specialty)
class AdminSpecialty(TabbedTranslationAdmin):
    model = Specialty



