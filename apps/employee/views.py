from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Employee, Position


class EmployeeListView(ListView):
    model = Employee
    context_object_name = 'employees'
    template_name = 'employee/index.html'
    paginate_by = 20

    def get_queryset(self):
        return Employee.active.select_related('position')


class EmployeeDetailView(DetailView):
    model = Employee
    queryset = model.active.select_related('position')
    slug_field = 'slug'
    context_object_name = 'employee'
    template_name = 'employee/employee_detail.html'
