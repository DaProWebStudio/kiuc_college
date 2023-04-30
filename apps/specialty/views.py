from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.utils.translation import gettext_lazy as _

from apps.specialty.models import Specialty


class SpecialtyListView(ListView):
    model = Specialty
    context_object_name = 'specialties'
    template_name = 'specialty/list.html'


class SpecialtyDetailView(DetailView):
    model = Specialty
    context_object_name = 'specialty'
    template_name = 'specialty/detail.html'
