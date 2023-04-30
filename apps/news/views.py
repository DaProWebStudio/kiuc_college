from django.db.models import Prefetch
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.utils.translation import gettext_lazy as _

from apps.news.models import News, NewsImages


class NewsListView(ListView):
    model = News
    queryset = model.active.all()
    context_object_name = 'news'
    template_name = 'news/list.html'


class NewsDetailView(DetailView):
    model = News
    queryset = model.active.prefetch_related(
        Prefetch('images', NewsImages.objects.only('image'))
    )
    context_object_name = 'item'
    template_name = 'news/detail.html'
