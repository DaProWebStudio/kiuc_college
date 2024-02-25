from django.urls import path, include
from apps.student import views

urlpatterns = [
    path('', views.StudentCouncilView.as_view(), name='students'),
    path('detail/<slug:slug>/', views.StudentDetailView.as_view(), name='students_detail'),
    path('saejeons/', views.SaeJeonListView.as_view(), name='saejeon_list'),
    path('saejeons/<slug:slug>/', views.SaeJeonDetailView.as_view(), name='saejeon_detail'),
]
