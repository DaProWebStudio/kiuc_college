from django.contrib import admin

from modeltranslation.admin import TabbedTranslationAdmin

from apps.news.models import NewsImages, News


class AdminNewsImages(admin.TabularInline):
    model = NewsImages
    extra = 1


@admin.register(News)
class AdminNews(TabbedTranslationAdmin):
    model = News
    # prepopulated_fields = {'slug': ('title',)}
    inlines = [AdminNewsImages]
