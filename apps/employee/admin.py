from django.contrib import admin
from .models import (
    Position, Employee, EmployeeEducation, Group, EmployeeLanguages,
    EmployeeWorkExperience, EmployeeAwards, EmployeeSkillUp
)

from common.utils import get_english_translit as get_slug


class EmployeeEducationInline(admin.TabularInline):
    """ Образование """
    model = EmployeeEducation
    extra = 1


class EmployeeWorkExperienceInline(admin.TabularInline):
    """ Опыт работы """
    model = EmployeeWorkExperience
    extra = 1


class EmployeeAwardsInline(admin.TabularInline):
    """ Награда """
    model = EmployeeAwards
    extra = 1


class EmployeeLanguagesInline(admin.TabularInline):
    """ Знание языков """
    model = EmployeeLanguages
    extra = 1


class EmployeeSkillUpInline(admin.TabularInline):
    """ Повышение квалификации """
    model = EmployeeSkillUp
    extra = 1


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """ Должность """
    list_display = ('title', 'short_title', 'created')


@admin.register(Employee)
class AdminEmployee(admin.ModelAdmin):
    list_display = ('get_full_name', 'position', 'number', 'is_active', 'created')
    list_filter = ('position', 'is_active')
    search_fields = ['get_full_name', 'position']
    fieldsets = (
        ('Необходимые данные:', {
            'fields': (('last_name', 'first_name', 'sur_name'), ('position', 'number', 'image',)),
        }),
        ('О себе:', {
            'fields': (('nationality', 'marital_status', 'date_of_birth', 'gender'), 'goal', 'work_skills'),
        }),
        ('Соц. сети:', {
            'fields': (('email', 'instagram', 'facebook'))
        }),
        ('Статус:', {
            'fields': ('is_active',)
        })
    )
    exclude = ('slug',)
    inlines = [
        EmployeeEducationInline,
        EmployeeWorkExperienceInline,
        EmployeeAwardsInline,
        EmployeeLanguagesInline,
        EmployeeSkillUpInline
    ]


@admin.register(Group)
class AdminGroup(admin.ModelAdmin):
    list_display = ('title', 'course', 'specialty', 'created', 'updated')
    list_filter = ('course', 'specialty')
    exclude = ('slug',)

    def save_model(self, request, obj, form, change):
        obj.slug = get_slug(obj.name)
        super().save_model(request, obj, form, change)
