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
    while True:
        pk = randint(1, max_id)
        item = model.objects.filter(pk=pk).first()
        if item:
            return item
