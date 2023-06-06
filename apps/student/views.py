from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import StudentCouncil


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
