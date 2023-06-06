from django.db import models
from django.urls import reverse

from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from ckeditor.fields import RichTextField

from common.utils import get_english_translit as get_slug
from common.upload_to_files import news_main_img, news_news_img
from common.managers import ActiveManager


class AbstractNews(models.Model):
    title = models.CharField(_('Название'), max_length=200)
    slug = models.SlugField("URL", max_length=255, null=True, blank=True)
    description = RichTextField(_('Описание'), blank=True, null=True)
    youtube = models.URLField(_('Ссылка на видео'), null=True, blank=True)

    is_active = models.BooleanField(_('Статус'), default=True)

    objects = models.Manager()
    active = ActiveManager()

    created = models.DateTimeField(_("Создано"))
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.title)
        super().save(*args, **kwargs)


class News(AbstractNews):
    """Новости колледжа"""
    image = ProcessedImageField(verbose_name=_('Фото'), upload_to=news_main_img, format='webp',
                                processors=[ResizeToFill(2268, 1296)], options={'quality': 90})

    def get_absolute_url(self, **kwargs):
        return reverse('news_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Новость')
        verbose_name_plural = _('Новости')


class NewsImages(models.Model):
    """Фотографии Новостях"""
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = ProcessedImageField(verbose_name=_('Фотография'), upload_to=news_news_img,
                                format='webp', options={'quality': 80})

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.news.title

    class Meta:
        ordering = ('created',)
        verbose_name = _('Фотография')
        verbose_name_plural = _('Фотографии')
