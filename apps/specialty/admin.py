from django.contrib import admin

from apps.specialty.models import Specialty


@admin.register(Specialty)
class AdminSpecialty(admin.ModelAdmin):
    exclude = ('slug',)
