from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from common.upload_to_files import recaptcha_img


class FeedBack(models.Model):
    """ Обратная связь """
    name = models.CharField(_('Ваше имя'), max_length=50)
    email = models.EmailField(_('Ваша электронная почта'))
    message = models.TextField(_('Ваше сообщение'))
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Обратная связь')
        verbose_name_plural = _('Обратная связь')


class Recaptcha(models.Model):
    """ ReCaptcha """
    image = ProcessedImageField(verbose_name=_('Изображение в Формате JPG 60X350'),
                                upload_to=recaptcha_img, format='webp',
                                processors=[ResizeToFill(350, 60)], options={'quality': 90})
    answer = models.IntegerField(_('Ответ'))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ответ - {str(self.answer)}"

    class Meta:
        ordering = ('-created',)
        verbose_name = 'ReCaptcha'
        verbose_name_plural = 'ReCaptcha'
