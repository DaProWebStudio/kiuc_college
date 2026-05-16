from django.db.models import Prefetch, Q
from django.urls import reverse
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.utils.translation import gettext_lazy as _

from apps.news.models import News, NewsImages


class NewsListView(ListView):
    model = News
    context_object_name = 'news'
    template_name = 'news/list.html'
    paginate_by = 12

    def get_queryset(self):
        qs = News.active.all()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = _('Новости')
        context['sub_title'] = _('Новости колледжа')
        context['q'] = self.request.GET.get('q', '').strip()
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
        context['breadcrumbs'] = [
            {'title': _('Новости'), 'url': reverse('news_list')},
            {'title': self.object.title},
        ]
        return context
