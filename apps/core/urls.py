from django.urls import path, include
from apps.core import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('history/', views.HistoryView.as_view(), name='history'),
]
