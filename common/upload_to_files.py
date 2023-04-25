from common.utils import get_english_translit as get_slug


def specialty_main_img(instance, filename):
    list_file = filename.split('.')
    return f'specialty/{instance.slug[:25]}.{list_file[-1]}'


def news_main_img(instance, filename):
    list_file = filename.split('.')
    title = instance.slug[0:35]
    return f'news/{title}/{title}.{list_file[-1]}'


def news_news_img(instance, filename):
    list_file = filename.split('.')
    return f'news/{instance.news.slug[0:35]}/{instance.news.slug[0:35]}.{list_file[-1]}'


def cooperation_files(instance, filename):
    list_file = filename.split('.')
    title = get_slug(instance.title)
    return f'cooperation/{title}/{title}.{list_file[-1]}'


def document_files(instance, filename):
    list_file = filename.split('.')
    return f'documents/{get_slug(instance.document.title)}/{get_slug(instance.title)}.{list_file[-1]}'


def recaptcha(instance, filename):
    list_file = filename.split('.')
    return f'recaptcha/{get_slug(list_file[0])}.{list_file[-1]}'


def employee_file(instance, filename):
    list_file = filename.split('.')
    return f'employees/{instance.slug}/{instance.slug}.{list_file[-1]}'
