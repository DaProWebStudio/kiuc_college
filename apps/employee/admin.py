from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Position, Nationality, Employee


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """ Должность """
    list_display = ('title', 'short_title', 'created')


@admin.register(Nationality)
class NationalityAdmin(admin.ModelAdmin):
    """ Национальность """
    list_display = ('title',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'position', 'number', 'is_active', 'created', 'get_photo')
    list_filter = ('position', 'is_active')
    search_fields = ['get_full_name', 'position']
    readonly_fields = ('get_photo',)

    fieldsets = (
        ('Необходимые данные:', {
            'fields': (
                'number',
                ('last_name', 'first_name', 'sur_name'),
                ('position', 'image', 'get_photo',),
                ('nationality', 'date_of_birth', 'gender'),
                'work_skills', 'description',
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
