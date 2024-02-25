from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from apps.core.models import AbstractResume
from apps.news.models import AbstractNews
from common.upload_to_files import student_file, saejeon_image, saejeon_images


class StudentCouncil(AbstractResume):
    """ Студентский совет """
    position = models.CharField(verbose_name=_('Должность'), max_length=255)
    image = ProcessedImageField(verbose_name=_('Фото студента'), upload_to=student_file, format='webp',
                                processors=[ResizeToFill(500, 500)], options={'quality': 90})

    def get_absolute_url(self):
        return reverse('students_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('number',)
        verbose_name = _('Студентский совет')
        verbose_name_plural = _('Студентский совет')


class SaeJeon(AbstractNews):
    """Сокулук Сэджон"""
    image = ProcessedImageField(verbose_name=_('Фото'), upload_to=saejeon_image, format='webp',
                                processors=[ResizeToFill(2268, 1296)], options={'quality': 90})

    def get_absolute_url(self, **kwargs):
        return reverse('saejeon_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Сокулук Сэджон')
        verbose_name_plural = _('Сокулук Сэджон')


class SaeJeonImages(models.Model):
    """Фотографии live"""
    saejeon = models.ForeignKey(SaeJeon, on_delete=models.CASCADE, related_name='images')
    image = ProcessedImageField(verbose_name=_('Фотография'), upload_to=saejeon_images,
                                format='webp', options={'quality': 80})

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.saejeon.title

    class Meta:
        ordering = ('created',)
        verbose_name = _('Фотография')
        verbose_name_plural = _('Фотографии')
