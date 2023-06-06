from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from apps.core.models import AbstractResume
from common.upload_to_files import student_file


class StudentCouncil(AbstractResume):
    """ Студентский совет """
    position = models.CharField(verbose_name=_('Должность'), max_length=255)
    image = ProcessedImageField(verbose_name=_('Фото студента'), upload_to=student_file, format='webp',
                                processors=[ResizeToFill(500, 500)], options={'quality': 90}, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('students_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('number',)
        verbose_name = _('Студентский совет')
        verbose_name_plural = _('Студентский совет')