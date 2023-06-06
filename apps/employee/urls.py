from django.urls import path, include
from apps.employee import views

urlpatterns = [
    path('', views.EmployeeListView.as_view(), name='employees'),
    path('detail/<slug:slug>/', views.EmployeeDetailView.as_view(), name='employees_detail'),
]
