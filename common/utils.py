from random import randint
import transliterate

from django.db.models import Max
from django.utils.text import slugify


def get_english_translit(text: str, slug: bool = True):
    letters = {'ң': 'н', 'ү': 'y', 'ө': 'о'}
    for key, value in letters.items():
        text = text.replace(key, value)
    try:
        translit = transliterate.translit(text, reversed=True)
    except transliterate.exceptions.LanguageDetectionError:
        translit = text
    return slugify(translit) if slug else translit


def get_random_model(model):
    max_id = model.objects.all().aggregate(max_id=Max("id"))['max_id']
    if max_id is None:
        return None
    while True:
        pk = randint(1, max_id)
        item = model.objects.filter(pk=pk).first()
        if item:
            return item


def get_unique_slug(instance, text: str) -> str:
    """Slug из text; занятый другой записью той же модели получает суффикс -2, -3, …

    Detail-страницы ищут запись по slug: два одинаковых заголовка давали один slug
    и MultipleObjectsReturned (500) на обеих страницах.
    """
    base = get_english_translit(text)
    max_length = instance._meta.get_field('slug').max_length
    others = type(instance)._base_manager.exclude(pk=instance.pk)
    slug, n = base[:max_length], 2
    while others.filter(slug=slug).exists():
        suffix = f'-{n}'
        slug = base[:max_length - len(suffix)] + suffix
        n += 1
    return slug
