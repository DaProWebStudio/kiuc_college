from django.urls import path, include
from apps.core import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('cooperation/', views.CooperationView.as_view(), name='cooperation'),
    # Documents
    path('documents/', views.DocumentListView.as_view(), name='documents_list'),
    path('documents/<int:pk>/', views.DocumentDetailView.as_view(), name='documents_detail'),
]
