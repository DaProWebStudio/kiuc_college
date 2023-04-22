from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from ckeditor.fields import RichTextField

from common.upload_to_files import upload_to_file
from common.utils import get_english_translit as get_slug
from common.managers import ActiveManager
from common import constants as cons


class Position(models.Model):
    """ Должность """
    title = models.CharField(_('Название'), max_length=100, unique=True)
    short_title = models.CharField(_('Короткое название'), max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Должность')
        verbose_name_plural = _('Должности')

    def get_short_name(self):
        return self.short_title if self.short_title is not None else self.title

    def __str__(self):
        return self.title


class Employee(models.Model):
    """ Работник """
    NATIONALITY_CHOICES = (
        (cons.KAZAKHSTAN, _('Кыргыз')),
        (cons.RUSSIA, _('Русский')),
        (cons.KAZAKHSTAN, _('Казах')),
    )

    MARITAL_STATUS_CHOICES = (
        (cons.NOT_MARRIED_MEN, _('не женат')),
        (cons.MARRIED_MEN, _('женат')),
        (cons.NOT_MARRIED_WOMEN, _('не замужем')),
        (cons.MARRIED_WOMEN, _('замужем')),
        (cons.DIVORCED, _('разведен(а)')),
    )

    GENDER_CHOICES = (
        (cons.MEN, _('Мужской')),
        (cons.WOMEN, _('Женский'))
    )

    number = models.IntegerField(_('Порядковый номер'), null=True, blank=True, default=100)
    last_name = models.CharField(_('Фамилия'), max_length=20)
    first_name = models.CharField(_('Имя'), max_length=20)
    sur_name = models.CharField(_('Отчество'), max_length=20, null=True, blank=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    position = models.ForeignKey(Position, verbose_name=_('Должность'), on_delete=models.PROTECT, related_name='resume')
    gender = models.CharField(_('Пол'), max_length=10, choices=GENDER_CHOICES, default=cons.MEN)
    date_of_birth = models.DateField(_('День рождения'))
    nationality = models.CharField(_('Национальность'), max_length=10,
                                   choices=NATIONALITY_CHOICES, default=cons.KAZAKHSTAN)
    marital_status = models.CharField(_('Семейное положение'), max_length=25,
                                      choices=MARITAL_STATUS_CHOICES, default=cons.NOT_MARRIED_MEN)
    goal = models.TextField(_('Цель'), null=True, blank=True)
    work_skills = models.TextField(_('Навыки работы'))
    image = ProcessedImageField(verbose_name=_('Фото сотрудника '), upload_to=upload_to_file, format='webp',
                                processors=[ResizeToFill(500, 500)], options={'quality': 90}, blank=True, null=True)

    email = models.EmailField('Email', blank=True, null=True)
    instagram = models.URLField('instagram', blank=True, null=True)
    facebook = models.URLField('facebook', blank=True, null=True)

    is_active = models.BooleanField("Активный", default=True)

    objects = models.Manager()
    active = ActiveManager()

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def get_full_name(self):
        if self.sur_name:
            return f'{self.last_name} {self.first_name} {self.sur_name}'
        return f'{self.last_name} {self.first_name}'

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.get_full_name())
        super(Employee, self).save(*args, **kwargs)

    def nationality_v(self):
        return dict(self.NATIONALITY_CHOICES)[self.nationality]

    def marital_status_v(self):
        return dict(self.MARITAL_STATUS_CHOICES)[self.marital_status]

    def get_absolute_url(self):
        return reverse('employee', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.sur_name if self.sur_name else ""}'

    class Meta:
        ordering = ('number',)
        verbose_name = _('Преподаватель')
        verbose_name_plural = _('Преподаватели')


class EmployeeEducation(models.Model):
    """ Образование """
    employee = models.ForeignKey(Employee, verbose_name=_('Сотрудник'), on_delete=models.CASCADE)
    start_year = models.PositiveSmallIntegerField(_('Начальный год'))
    year_of_release = models.PositiveSmallIntegerField(_('Год выпуска'))
    name = models.CharField(_('Название ВУЗа или СПО'), max_length=255)
    direction = models.CharField(_('Направление'), max_length=255)

    def __str__(self) -> str:
        return f'{self.employee} - {self.name}'

    class Meta:
        ordering = ('start_year',)
        verbose_name = _('Образование')
        verbose_name_plural = _('Образовании')


class EmployeeWorkExperience(models.Model):
    """ Опыт работы """
    employee = models.ForeignKey(Employee, verbose_name=_('Сотрудник'), on_delete=models.CASCADE)
    start_year = models.PositiveSmallIntegerField(_('Начальный год'))
    year_of_release = models.PositiveSmallIntegerField(_('Год выпуска'))
    name = models.CharField(_('Название организации'), max_length=255)
    position = models.CharField(_('Должность'), max_length=255)

    def __str__(self) -> str:
        return f'{self.employee} - {self.name}'

    class Meta:
        ordering = ('start_year',)
        verbose_name = _('Опыт работы')
        verbose_name_plural = _('Опыты работы')


class EmployeeAwards(models.Model):
    """ Награда """
    employee = models.ForeignKey(Employee, verbose_name=_('Сотрудник'), on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(_('Год'))
    name = models.CharField(_('Название организации'), max_length=255)
    award = models.CharField(_('Описание награды'), max_length=255)

    def __str__(self) -> str:
        return f'{self.employee} - {self.name}'

    class Meta:
        ordering = ('year',)
        verbose_name = _('Награда')
        verbose_name_plural = _('Награды')


class EmployeeLanguages(models.Model):
    """ Знание языков """
    LANGUAGE_CHOICES = (
        (cons.KYRGYZSTAN, _('Кыргызский')),
        (cons.KAZAKHSTAN, _('Казахский')),
        (cons.RUSSIA, _('Русский')),
        (cons.ENGLISH, _('Английский')),
        (cons.GERMAN, _('Немецкий')),
    )

    employee = models.ForeignKey(Employee, verbose_name=_('Сотрудник'), on_delete=models.CASCADE)
    language = models.CharField(_('Язык'), max_length=10, choices=LANGUAGE_CHOICES)

    def title(self):
        return dict(self.LANGUAGE_CHOICES)[self.language]

    def __str__(self) -> str:
        return f'{self.employee} - {self.language}'

    class Meta:
        verbose_name = _('Язык')
        verbose_name_plural = _('Языки')


class EmployeeSkillUp(models.Model):
    """ Повышение квалификации """
    employee = models.ForeignKey(Employee, verbose_name=_('Сотрудник'), on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField(_('Год'))
    description = models.TextField(_('Описание по повышению квалификации'))

    def __str__(self) -> str:
        return f'{self.employee} - {self.description}'

    class Meta:
        ordering = ('year',)
        verbose_name = _('Повышение квалификацию')
        verbose_name_plural = _('Повышение квалификации')


class Group(models.Model):
    COURSE = (
        (cons.COURSE_1, _('1-курс')),
        (cons.COURSE_2, _('2-курс')),
        (cons.COURSE_3, _('3-курс')),
        (cons.COURSE_4, _('4-курс')),
    )

    title = models.CharField(_('Имя группы'), max_length=20)
    slug = models.SlugField("URL")
    course = models.CharField(_('Курс'), max_length=10, choices=COURSE, default='1-course')
    specialty = models.ForeignKey('specialty.Specialty', verbose_name=_('Специальность'), on_delete=models.CASCADE,
                                  related_name='groups')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('course',)
        verbose_name = _('Группа')
        verbose_name_plural = _('Группы')
