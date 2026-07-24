from django.conf import settings
from django.utils.functional import SimpleLazyObject

from apps.core.models import EduProcess, SiteContact


def getting_info(request):
    style_core_version = settings.STYLE_CORE_VERSION
    style_responsive_version = settings.STYLE_RESPONSIVE_VERSION
    edu_processes = EduProcess.active.all()
    # Lazy: запрос уходит в БД только когда шаблон реально обращается к контактам.
    site_contacts = SimpleLazyObject(SiteContact.load)
    return locals()
