from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.utils.translation import gettext_lazy as _

from apps.news.models import News
from apps.specialty.models import Specialty


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["specialties"] = Specialty.active.all()
        context["news"] = News.active.all()[:9]
        return context


class HistoryView(TemplateView):
    template_name = 'history.html'
