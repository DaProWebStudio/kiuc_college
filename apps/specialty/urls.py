from django.urls import path
from apps.specialty import views

urlpatterns = [
    path('', views.SpecialtyListView.as_view(), name='specialties_list'),
    path('<int:pk>/', views.SpecialtyDetailView.as_view(), name='specialties_detail'),
]
