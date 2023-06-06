from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Employee, Position


class EmployeeListView(ListView):
    model = Employee
    queryset = model.active.select_related('position')
    context_object_name = 'employees'
    template_name = 'employee/index.html'


class EmployeeDetailView(DetailView):
    model = Employee
    queryset = model.active.select_related('position')
    slug_field = 'slug'
    context_object_name = 'employee'
    template_name = 'employee/employee_detail.html'
