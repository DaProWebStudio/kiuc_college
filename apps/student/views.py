from django.db.models import Prefetch
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from .models import StudentCouncil, SaeJeon, SaeJeonImages


class StudentCouncilView(ListView):
    model = StudentCouncil
    context_object_name = 'students'
    template_name = 'student/index.html'
    paginate_by = 20

    def get_queryset(self):
        return StudentCouncil.active.all()


class StudentDetailView(DetailView):
    model = StudentCouncil
    queryset = model.active.all()
    slug_field = 'slug'
    context_object_name = 'student'
    template_name = 'student/student_detail.html'


class SaeJeonListView(ListView):
    model = SaeJeon
    context_object_name = 'news'
    template_name = 'news/list.html'
    paginate_by = 12

    def get_queryset(self):
        qs = SaeJeon.active.all()
        q = self.request.GET.get('q', '').strip()
        if q:
            from django.db.models import Q
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = _('Сокулук Сэджон')
        context['sub_title'] = _('Студентам')
        context['q'] = self.request.GET.get('q', '').strip()
        return context


class SaeJeonDetailView(DetailView):
    model = SaeJeon
    queryset = model.active.prefetch_related(
        Prefetch('images', SaeJeonImages.objects.only('image'))
    )
    context_object_name = 'item'
    template_name = 'news/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Сокулук Сэджон')
        return context
