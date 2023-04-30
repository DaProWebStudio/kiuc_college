from django.contrib import admin
from django.utils.safestring import mark_safe

from modeltranslation.admin import TabbedTranslationAdmin

from apps.news.models import NewsImages, News


class AdminNewsImages(admin.TabularInline):
    model = NewsImages
    extra = 1
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="75">')

    get_photo.short_description = "Миниатюра"


@admin.register(News)
class AdminNews(TabbedTranslationAdmin):
    model = News
    list_display = ('title', 'is_active', 'get_photo')
    inlines = [AdminNewsImages]
    readonly_fields = ('get_photo',)

    exclude = ('slug',)

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="75">')

    get_photo.short_description = "Миниатюра"
