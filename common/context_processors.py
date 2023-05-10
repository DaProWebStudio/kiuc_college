from django.conf import settings


def getting_info(request):
    style_core_version = settings.STYLE_CORE_VERSION
    style_responsive_version = settings.STYLE_RESPONSIVE_VERSION
    return locals()
