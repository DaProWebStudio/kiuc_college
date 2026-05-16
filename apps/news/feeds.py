from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import gettext_lazy as _

from apps.news.models import News


class NewsRSSFeed(Feed):
    title = _('Новости КМУК')
    description = _('Последние новости и события Кыргызского международного универсального колледжа.')

    def link(self):
        return reverse('news_list')

    def items(self):
        return News.active.all()[:30]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description or ''

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.created


class NewsAtomFeed(NewsRSSFeed):
    feed_type = Atom1Feed
    subtitle = NewsRSSFeed.description
