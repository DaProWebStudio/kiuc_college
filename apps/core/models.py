from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from common.upload_to_files import document_files, cooperation_files


class Cooperation(models.Model):
    """Сотрудничество"""
    title = models.CharField(_("Название"), max_length=255)
    is_international = models.BooleanField(_("Является международным"), default=False)
    file = models.FileField(_("Файл"), validators=[FileExtensionValidator(['pdf'])], upload_to=cooperation_files)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Сотрудничество')
        verbose_name_plural = _('Сотрудничество')


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
