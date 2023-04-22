from django.utils.text import slugify
import transliterate


def get_english_translit(text: str, slug: bool = True):
    letters = {'ң': 'н', 'ү': 'y', 'ө': 'о'}
    for key, value in letters.items():
        text = text.replace(key, value)
    try:
        translit = transliterate.translit(text, reversed=True)
    except transliterate.exceptions.LanguageDetectionError:
        translit = text
    return slugify(translit) if slug else translit
