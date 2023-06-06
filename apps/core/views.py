from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, ListView, DetailView
from django.utils.translation import gettext_lazy as _

from apps.core.models import Cooperation, Document, DocumentFile, InternationalCooperation, \
    InternationalCooperationImages, EduProcess, EduProcessFile
from apps.news.models import News
from apps.specialty.models import Specialty
from apps.employee.models import Employee
from apps.student.models import StudentCouncil, StudentLive


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["specialties"] = Specialty.active.all()
        context["news"] = News.active.all()[:9]
        context["lives"] = StudentLive.active.all()[:9]
        context["employees"] = Employee.active.select_related('position')[:9]
        context["students"] = StudentCouncil.active.all()[:9]
        context["internationals"] = InternationalCooperation.objects.all()
        return context


class HistoryView(TemplateView):
    template_name = 'history.html'


class PasswordCollegeView(TemplateView):
    template_name = 'passport-college.html'


class DocumentListView(ListView):
    model = Document
    queryset = model.objects.all()
    context_object_name = 'documents'
    template_name = 'documents/list.html'


class DocumentDetailView(DetailView):
    model = Document
    queryset = model.objects.prefetch_related(
        Prefetch('files', DocumentFile.objects.all())
    )
    context_object_name = 'document'
    template_name = 'documents/detail.html'


class CooperationView(ListView):
    model = Cooperation
    queryset = model.objects.all()
    context_object_name = 'cooperation'
    template_name = 'collaborations/cooperation.html'


class InternationalCooperationListView(ListView):
    model = InternationalCooperation
    context_object_name = 'internationals'
    template_name = 'collaborations/internationals.html'


class InternationalCooperationDetailView(DetailView):
    model = InternationalCooperation
    queryset = model.objects.prefetch_related(
        Prefetch('images', InternationalCooperationImages.objects.only('image'))
    )
    slug_field = 'slug'
    context_object_name = 'international'
    template_name = 'collaborations/international-detail.html'


class WelcomingRemarksView(TemplateView):
    template_name = 'welcoming-remarks.html'


class ReceptionApplicantsView(ListView):
    model = Specialty
    queryset = model.active.all()
    context_object_name = 'specialties'
    template_name = 'reception.html'


class EduProcessDetailView(DetailView):
    model = EduProcess
    queryset = model.objects.prefetch_related(
        Prefetch('files', EduProcessFile.objects.all())
    )
    context_object_name = 'process'
    template_name = 'edu_process_detail.html'

