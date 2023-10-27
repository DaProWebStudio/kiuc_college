from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from apps.core.models import AbstractResume
from apps.news.models import AbstractNews
from common.upload_to_files import student_file, student_live, student_live_images


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


class StudentLive(AbstractNews):
    """Студентская жизнь"""
    image = ProcessedImageField(verbose_name=_('Фото'), upload_to=student_live, format='webp',
                                processors=[ResizeToFill(2268, 1296)], options={'quality': 90})

    def get_absolute_url(self, **kwargs):
        return reverse('student_live_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Студентская жизнь')
        verbose_name_plural = _('Студентская жизнь')


class StudentLiveImages(models.Model):
    """Фотографии live"""
    live = models.ForeignKey(StudentLive, on_delete=models.CASCADE, related_name='images')
    image = ProcessedImageField(verbose_name=_('Фотография'), upload_to=student_live_images,
                                format='webp', options={'quality': 80})

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.live.title

    class Meta:
        ordering = ('created',)
        verbose_name = _('Фотография')
        verbose_name_plural = _('Фотографии')
