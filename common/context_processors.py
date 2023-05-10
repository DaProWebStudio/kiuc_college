from django.conf import settings

from apps.core.models import EduProcess


def getting_info(request):
    style_core_version = settings.STYLE_CORE_VERSION
    style_responsive_version = settings.STYLE_RESPONSIVE_VERSION
    edu_processes = EduProcess.active.all()
    return locals()
