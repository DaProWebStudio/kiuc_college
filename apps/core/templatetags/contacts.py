"""Контакты для шаблонов, которые рендерятся без context processors."""
from django import template
from django.db import DatabaseError

from apps.core.models import SiteContact

register = template.Library()


@register.simple_tag
def site_contacts():
    """Singleton с контактами. Для 500.html: страница обязана отрисоваться даже
    когда БД недоступна, поэтому при ошибке отдаём несохранённый экземпляр
    со значениями по умолчанию."""
    try:
        return SiteContact.load()
    except DatabaseError:
        return SiteContact()
