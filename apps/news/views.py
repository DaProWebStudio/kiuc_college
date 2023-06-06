from django.db.models import Prefetch
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.utils.translation import gettext_lazy as _

from apps.news.models import News, NewsImages


class NewsListView(ListView):
    model = News
    queryset = model.active.all()
    context_object_name = 'news'
    template_name = 'news/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = _('Новости')
        context['sub_title'] = _('Новости колледжа')
        return context


class NewsDetailView(DetailView):
    model = News
    queryset = model.active.prefetch_related(
        Prefetch('images', NewsImages.objects.only('image'))
    )
    context_object_name = 'item'
    template_name = 'news/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Новости')
        return context
