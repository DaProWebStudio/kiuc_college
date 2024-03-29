"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import settings

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('specialties/', include('apps.specialty.urls')),
    path('contacts/', include('apps.feedback.urls')),
    path('employee/', include('apps.employee.urls')),
    path('students/', include('apps.student.urls')),
    path('news/', include('apps.news.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += (
        static(settings.STATIC_URL, document_root=settings.STATIC_DIR) +
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
