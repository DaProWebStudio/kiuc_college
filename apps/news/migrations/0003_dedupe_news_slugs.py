"""Разводит совпавшие slug у новостей («День студента в КМУК!» 2024 и 2025 и т.п.).

slug строится из заголовка, а NewsDetailView ищет по нему: при совпадении обе
страницы отдавали 500 (MultipleObjectsReturned). Старшая запись (меньший id)
сохраняет адрес, следующие получают -2, -3, … — так же, как теперь при
сохранении делает common.utils.get_unique_slug.
"""
from django.db import migrations
from django.db.models import Count


def dedupe_slugs(apps, schema_editor):
    News = apps.get_model('news', 'News')
    max_length = News._meta.get_field('slug').max_length
    dup_slugs = list(
        News.objects.order_by()
        .exclude(slug__isnull=True).exclude(slug='')
        .values('slug').annotate(n=Count('id')).filter(n__gt=1)
        .values_list('slug', flat=True)
    )
    for base in dup_slugs:
        for news in list(News.objects.filter(slug=base).order_by('id'))[1:]:
            n = 2
            while True:
                suffix = f'-{n}'
                slug = base[:max_length - len(suffix)] + suffix
                if not News.objects.filter(slug=slug).exists():
                    break
                n += 1
            News.objects.filter(pk=news.pk).update(slug=slug)


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_news_slug_alter_news_title_alter_news_title_en_and_more'),
    ]

    operations = [
        migrations.RunPython(dedupe_slugs, migrations.RunPython.noop),
    ]
