from django.urls import path
from apps.feedback import views

urlpatterns = [
    path('', views.ContactsView.as_view(), name='contacts'),
]
