from django.urls import path, include
from apps.core import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('password-college/', views.PasswordCollegeView.as_view(), name='password_college'),
    # Documents
    path('documents/', views.DocumentListView.as_view(), name='documents_list'),
    path('documents/<int:pk>/', views.DocumentDetailView.as_view(), name='documents_detail'),
    # Collaborations
    path('cooperation/', views.CooperationView.as_view(), name='cooperation'),
    path('internationals/', views.InternationalCooperationListView.as_view(), name='internationals'),
    path('internationals/<slug:slug>/', views.InternationalCooperationDetailView.as_view(), name='international_detail'),
    # More
    path('welcoming-remarks/', views.WelcomingRemarksView.as_view(), name='welcoming_remarks'),
    path('reception-applicants/', views.ReceptionApplicantsView.as_view(), name='reception'),
    # Education Process
    path('education-processes/<int:pk>/', views.EduProcessDetailView.as_view(), name='edu_process_detail'),
]
