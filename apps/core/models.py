from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator


class Cooperation(models.Model):
    """Сотрудничество"""
    title = models.CharField(_("Название"), max_length=255)
    is_international = models.BooleanField(_("Является международным"), default=False)
    file = models.FileField(_("Файл"), validators=[FileExtensionValidator(['pdf'])])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Сотрудничество')
        verbose_name_plural = _('Сотрудничество')
