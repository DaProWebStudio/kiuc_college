from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from modeltranslation.admin import TabbedTranslationAdmin

from .models import (
    Cooperation,
    InternationalCooperation,
    InternationalCooperationImages,
    Document,
    DocumentFile, EduProcessFile, EduProcess,
    ReceptionPage,
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


@admin.register(ReceptionPage)
class ReceptionPageAdmin(TabbedTranslationAdmin):
    """Singleton-страница «Абитуриентам». Один экземпляр, открывается сразу
    на редактирование без промежуточного changelist."""

    fieldsets = (
        ('Хиро (заголовок страницы)', {
            'fields': ('heading', 'lead'),
        }),
        ('Основной текст', {
            'fields': ('body',),
            'description': 'Большой блок с правилами поступления, стоимостью, требованиями к документам и т.п. '
                           'Поддерживает форматирование, списки, цитаты — всё через WYSIWYG.',
        }),
        ('Сайдбар «Контакты приёмной»', {
            'fields': ('contacts_title', 'contact_phone', 'contact_whatsapp',
                       'contact_email', 'contact_website_label', 'contact_website_url'),
        }),
    )

    def has_add_permission(self, request):
        return not ReceptionPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = ReceptionPage.objects.first()
        if obj:
            return redirect(reverse('admin:core_receptionpage_change', args=[obj.pk]))
        return super().changelist_view(request, extra_context)
