from django.urls import path, include
from apps.student import views

urlpatterns = [
    path('', views.StudentCouncilView.as_view(), name='students'),
    path('detail/<slug:slug>/', views.StudentDetailView.as_view(), name='students_detail'),
    path('live/', views.StudentLiveListView.as_view(), name='student_live_list'),
    path('live/<slug:slug>/', views.StudentLiveDetailView.as_view(), name='student_live_detail'),
]
