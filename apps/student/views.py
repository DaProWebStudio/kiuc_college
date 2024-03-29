from django.db.models import Prefetch
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from .models import StudentCouncil, SaeJeon, SaeJeonImages


class StudentCouncilView(ListView):
    model = StudentCouncil
    queryset = model.active.all()
    context_object_name = 'students'
    template_name = 'student/index.html'


class StudentDetailView(DetailView):
    model = StudentCouncil
    queryset = model.active.all()
    slug_field = 'slug'
    context_object_name = 'student'
    template_name = 'student/student_detail.html'


class SaeJeonListView(ListView):
    model = SaeJeon
    queryset = model.active.all()
    context_object_name = 'news'
    template_name = 'news/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = _('Сокулук Сэджон')
        context['sub_title'] = _('Студентам')
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
