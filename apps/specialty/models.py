from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from ckeditor.fields import RichTextField
from common.utils import get_english_translit as get_slug

from common import constants as cons
from common.managers import ActiveManager
from common.upload_to_files import specialty_main_img


class Specialty(models.Model):
    """Специальности"""
    TRAINING = (
        (cons.FULL_TIME, _('Очный')),
        (cons.FULL_AND_PART, _('Очный/Заочный')),
        (cons.PART_TIME, _('Заочный'))
    )
    LEARNING = (
        (cons.CONTRACT, _('Контракт')),
        (cons.CONTRACT_BUDGET, _('Контракт/Бюджет'))
    )
    name = models.CharField(_('Наименование'), max_length=350)
    slug = models.SlugField("URL", max_length=450, null=True, blank=True)
    body = RichTextField(_('Описание'))
    contract = models.CharField(_('Сумма контракта'), max_length=50)
    form_of_training = models.CharField(_('Форма обучение'), max_length=20, choices=TRAINING, default=cons.FULL_TIME)
    basis_learning = models.CharField(_('Основа обучения'), max_length=100, choices=LEARNING, default=cons.CONTRACT)
    image = ProcessedImageField(verbose_name=_('Фото'), upload_to=specialty_main_img, format='webp',
                                processors=[ResizeToFill(756, 432)], options={'quality': 90})
    is_active = models.BooleanField(_('Статус'), default=True)

    objects = models.Manager()
    active = ActiveManager()

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def form_verbose(self):
        return dict(Specialty.TRAINING)[self.form_of_training]

    def basis_verbose(self):
        return dict(Specialty.LEARNING)[self.basis_learning]

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.name)
        super(Specialty, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Специальность')
        verbose_name_plural = _('Специальности')
