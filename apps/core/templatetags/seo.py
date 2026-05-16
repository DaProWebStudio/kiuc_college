"""SEO + общие шаблонные хелперы."""
from django import template
from django.urls import translate_url as _translate_url
from django.utils.html import strip_tags
from django.utils.text import Truncator

register = template.Library()


@register.simple_tag
def pagination_range(page_obj, paginator):
    """Усечённый диапазон страниц вокруг текущей — для UI пагинатора."""
    return paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1)


@register.simple_tag(takes_context=True)
def is_active(context, *url_names, css_class='nav-link-active'):
    """Возвращает CSS-класс, если текущий url_name входит в переданный список."""
    match = context['request'].resolver_match
    if match and match.url_name in url_names:
        return css_class
    return ''


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
