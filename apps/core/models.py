from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from ckeditor.fields import RichTextField

from common.utils import get_english_translit as get_slug
from common.upload_to_files import document_files, cooperation_files, international_images, international_main_img
from common.managers import ActiveManager


class Cooperation(models.Model):
    """Сотрудничество"""
    title = models.CharField(_("Название"), max_length=255)
    file = models.FileField(_("Файл"), validators=[FileExtensionValidator(['pdf'])], upload_to=cooperation_files)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Сотрудничество')
        verbose_name_plural = _('Сотрудничество')


class InternationalCooperation(models.Model):
    """Международное сотрудничество"""
    title = models.CharField(_('Название'), max_length=230)
    slug = models.SlugField("URL", max_length=255, null=True, blank=True)
    description = RichTextField(_('Описание'), blank=True, null=True)
    image = ProcessedImageField(verbose_name=_('Фото'), upload_to=international_main_img, format='webp',
                                processors=[ResizeToFill(2268, 1296)], options={'quality': 90})

    objects = models.Manager()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.title)
        super(InternationalCooperation, self).save(*args, **kwargs)

    def get_absolute_url(self, **kwargs):
        return reverse('international_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Международное сотрудничество')
        verbose_name_plural = _('Международные сотрудничество')


class InternationalCooperationImages(models.Model):
    """Фотографии Международное сотрудничество"""
    international = models.ForeignKey(InternationalCooperation, on_delete=models.CASCADE, related_name='images')
    image = ProcessedImageField(verbose_name=_('Фотография'), upload_to=international_images, format='webp', options={'quality': 80})

    def __str__(self):
        return str(self.international.title)

    class Meta:
        verbose_name = _('Фотография')
        verbose_name_plural = _('Фотографии')


class Document(models.Model):
    title = models.CharField(_("Название"), max_length=255)
    is_active = models.BooleanField(_("Активный"), default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Нормативный документ')
        verbose_name_plural = _('Нормативные документы')


class DocumentFile(models.Model):
    document = models.ForeignKey(Document, verbose_name=_("Документ"), on_delete=models.CASCADE, related_name='files')
    title = models.CharField(_("Название файла"), max_length=255)
    file = models.FileField(
        _("Файл"), validators=[FileExtensionValidator(['pdf', 'png', 'jpg', 'webp'])], upload_to=document_files
    )

    def __str__(self):
        return f'{self.document} - {self.title}'

    class Meta:
        verbose_name = _('Файл документа')
        verbose_name_plural = _('Файлы документа')
