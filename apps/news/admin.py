from django.contrib import admin

from apps.news.models import NewsImages, News


class AdminNewsImages(admin.TabularInline):
    model = NewsImages
    extra = 1


@admin.register(News)
class AdminNews(admin.ModelAdmin):
    model = News
    inlines = [AdminNewsImages]
