from common.utils import get_english_translit as get_slug


def specialty_main_img(instance, filename):
    list_file = filename.split('.')
    return f'specialty/{get_slug(instance.name)}.{list_file[-1]}/'


def news_main_img(instance, filename):
    list_file = filename.split('.')
    return f'News/{instance.slug[0:35]}/{get_slug(list_file[0])}.{list_file[-1]}/'


def news_news_img(instance, filename):
    list_file = filename.split('.')
    return f'News/{instance.news.slug[0:35]}/{get_slug(list_file[0])}.{list_file[-1]}/'
