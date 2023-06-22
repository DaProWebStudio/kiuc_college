from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from apps.core.models import AbstractResume
from common.upload_to_files import employee_file
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
        return self.short_title if self.short_title else self.title

    def __str__(self):
        return self.title


class Employee(AbstractResume):
    """ Работник """
    NATIONALITY_CHOICES = (
        (cons.KYRGYZSTAN, _('Кыргыз')),
        (cons.RUSSIA, _('Русский')),
        (cons.KAZAKHSTAN, _('Казах')),
        (cons.KAZAKHSTAN, _('Кореец')),
    )
    position = models.ForeignKey(Position, verbose_name=_('Должность'), on_delete=models.PROTECT, related_name='resume')
    nationality = models.CharField(_('Национальность'), max_length=10,
                                   choices=NATIONALITY_CHOICES, default=cons.KYRGYZSTAN)
    work_skills = models.TextField(_('Навыки работы'))
    image = ProcessedImageField(verbose_name=_('Фото сотрудника'), upload_to=employee_file, format='webp',
                                processors=[ResizeToFill(500, 500)], options={'quality': 90}, blank=True, null=True)

    class Meta:
        ordering = ('number',)
        verbose_name = _('Преподаватель')
        verbose_name_plural = _('Преподаватели')

    def get_absolute_url(self):
        return reverse('employees_detail', kwargs={'slug': self.slug})

    def nationality_v(self):
        return dict(self.NATIONALITY_CHOICES)[self.nationality]

