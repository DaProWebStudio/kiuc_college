import uuid

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
    title = get_slug(instance.title[:30])
    return f'cooperation/{title}/{title}.{list_file[-1]}'


def international_main_img(instance, filename):
    list_file = filename.split('.')
    title = get_slug(instance.title[:30])
    return f'cooperation/internationals/{title}/main-{title}.{list_file[-1]}'


def international_pdf(instance, filename):
    list_file = filename.split('.')
    title = get_slug(instance.title[:30])
    return f'cooperation/internationals/{title}/{title}.{list_file[-1]}'


def international_images(instance, filename):
    list_file = filename.split('.')
    title = get_slug(instance.international.title[:30])
    print(title)
    return f'cooperation/internationals/{title}/{title}.{list_file[-1]}'


def document_files(instance, filename):
    list_file = filename.split('.')
    return f'documents/{get_slug(instance.document.title)}/{get_slug(instance.title)}.{list_file[-1]}'


def edu_process_files(instance, filename):
    list_file = filename.split('.')
    return f'edu-processes/{get_slug(instance.process.title)}/{get_slug(instance.title)}.{list_file[-1]}'


def recaptcha_img(instance, filename):
    list_file = filename.split('.')
    return f'recaptcha/{uuid.uuid4().hex[:12]}.{list_file[-1]}'


def employee_file(instance, filename):
    list_file = filename.split('.')
    return f'employees/{instance.slug}/{instance.slug}.{list_file[-1]}'


def student_file(instance, filename):
    list_file = filename.split('.')
    return f'students/{instance.slug}/{instance.slug}.{list_file[-1]}'


def student_live(instance, filename):
    list_file = filename.split('.')
    return f'students/live/{instance.slug[0:35]}/main.{list_file[-1]}'


def student_live_images(instance, filename):
    list_file = filename.split('.')
    return f'students/live/{instance.live.slug[0:35]}/images/{list_file[0]}.{list_file[-1]}'