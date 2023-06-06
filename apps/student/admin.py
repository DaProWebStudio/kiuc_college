from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TabbedTranslationAdmin

from .models import StudentCouncil, StudentLive, StudentLiveImages


@admin.register(StudentCouncil)
class StudentCouncilAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'position', 'number', 'created', 'get_photo')
    search_fields = ['get_full_name', 'position']
    readonly_fields = ('get_photo',)

    fieldsets = (
        ('Необходимые данные:', {
            'fields': (
                'number',
                ('last_name', 'first_name', 'sur_name'),
                ('position', 'image', 'get_photo',),
                ('date_of_birth', 'gender'),
                'description',
            ),
        }),
        ('Соц. сети:', {
            'fields': (('email', 'instagram', 'facebook'),)
        }),
        ('Статус:', {
            'fields': ('is_active',)
        })
    )
    exclude = ('slug',)

    def get_full_name(self, obj):
        """ Полное имя """
        if obj.sur_name:
            return f'{obj.last_name} {obj.first_name} {obj.sur_name}'
        return f'{obj.last_name} {obj.first_name}'

    get_full_name.short_description = "ФИО"

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="border-radius: 50%" width="75">')

    get_photo.short_description = "Миниатюра"


class StudentLiveImagesInline(admin.TabularInline):
    model = StudentLiveImages
    readonly_fields = ('get_photo',)
    extra = 1

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="75">')

    get_photo.short_description = "Миниатюра"


@admin.register(StudentLive)
class StudentLiveAdmin(TabbedTranslationAdmin):
    model = StudentLive
    list_display = ('title', 'is_active', 'get_photo')
    inlines = [StudentLiveImagesInline]
    readonly_fields = ('get_photo',)

    exclude = ('slug',)

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="75">')

    get_photo.short_description = "Миниатюра"
