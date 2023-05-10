from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TabbedTranslationAdmin

from .models import (
    Cooperation,
    InternationalCooperation,
    InternationalCooperationImages,
    Document,
    DocumentFile, EduProcessFile, EduProcess,
)


@admin.register(Cooperation)
class CooperationAdmin(admin.ModelAdmin):
    list_display = ('title',)


class InternationalImagesInline(admin.TabularInline):
    model = InternationalCooperationImages
    extra = 1
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="75">')

    get_photo.short_description = "Миниатюра"


@admin.register(InternationalCooperation)
class InternationalCooperationAdmin(TabbedTranslationAdmin):
    model = InternationalCooperation
    list_display = ('title', 'get_photo')
    inlines = [InternationalImagesInline]
    readonly_fields = ('get_photo',)

    exclude = ('slug',)

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="75">')

    get_photo.short_description = "Миниатюра"


class DocumentFileInlines(admin.TabularInline):
    model = DocumentFile
    extra = 1


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [DocumentFileInlines]


class EduProcessFileInlines(admin.TabularInline):
    model = EduProcessFile
    extra = 1


@admin.register(EduProcess)
class EduProcessAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [EduProcessFileInlines]
