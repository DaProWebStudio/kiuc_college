from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.core.models import InternationalCooperation, EduProcess
from apps.employee.models import Employee
from apps.news.models import News
from apps.specialty.models import Specialty
from apps.student.models import StudentCouncil, SaeJeon


class StaticPagesSitemap(Sitemap):
    """Статические страницы — без модели, по url-name."""
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return [
            "index",
            "history",
            "password_college",
            "welcoming_remarks",
            "reception",
            "documents_list",
            "cooperation",
            "internationals",
            "specialties_list",
            "employees",
            "students",
            "saejeon_list",
            "news_list",
            "contacts",
        ]

    def location(self, item):
        return reverse(item)


class _ModelSitemap(Sitemap):
    """Базовая sitemap для моделей с get_absolute_url + updated."""
    changefreq = "weekly"
    priority = 0.6

    model = None
    queryset_attr = "objects"

    def items(self):
        manager = getattr(self.model, self.queryset_attr)
        return manager.all()

    def lastmod(self, obj):
        return getattr(obj, "updated", None)


class NewsSitemap(_ModelSitemap):
    model = News
    queryset_attr = "active"
    priority = 0.8
    changefreq = "daily"


class SpecialtySitemap(_ModelSitemap):
    model = Specialty
    queryset_attr = "active"
    priority = 0.9
    changefreq = "monthly"


class SaeJeonSitemap(_ModelSitemap):
    model = SaeJeon
    queryset_attr = "active"


class EmployeeSitemap(_ModelSitemap):
    model = Employee
    queryset_attr = "active"


class StudentCouncilSitemap(_ModelSitemap):
    model = StudentCouncil
    queryset_attr = "active"


class InternationalSitemap(_ModelSitemap):
    model = InternationalCooperation
    priority = 0.7


class EduProcessSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return EduProcess.active.all()

    def location(self, item):
        return reverse("edu_process_detail", kwargs={"pk": item.pk})

    def lastmod(self, obj):
        return obj.updated


sitemaps = {
    "static": StaticPagesSitemap,
    "news": NewsSitemap,
    "specialties": SpecialtySitemap,
    "saejeon": SaeJeonSitemap,
    "employees": EmployeeSitemap,
    "students": StudentCouncilSitemap,
    "internationals": InternationalSitemap,
    "edu_processes": EduProcessSitemap,
}
