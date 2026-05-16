"""SEO-related template helpers."""
from django import template
from django.urls import translate_url as _translate_url
from django.utils.html import strip_tags
from django.utils.text import Truncator

register = template.Library()


@register.simple_tag(takes_context=True)
def alt_url(context, lang_code):
    """Текущий путь, переведённый в указанный язык — для hreflang."""
    request = context["request"]
    return _translate_url(request.path, lang_code)


@register.simple_tag(takes_context=True)
def absolute_url(context, path):
    """Префиксует относительный путь полным `scheme://host`."""
    request = context["request"]
    if path and path.startswith("http"):
        return path
    return f"{request.scheme}://{request.get_host()}{path or ''}"


@register.simple_tag(takes_context=True)
def site_origin(context):
    """Только `scheme://host` без пути — для конкатенации с {% static %}."""
    request = context["request"]
    return f"{request.scheme}://{request.get_host()}"


@register.filter
def seo_text(value, length=160):
    """HTML → plain → обрезает до length символов. Для meta description."""
    if not value:
        return ""
    return Truncator(strip_tags(value)).chars(length, truncate="…")
