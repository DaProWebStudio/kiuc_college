from django.contrib import admin
from .models import Cooperation, Document, DocumentFile


@admin.register(Cooperation)
class CooperationAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_international')
    list_filter = ('is_international',)