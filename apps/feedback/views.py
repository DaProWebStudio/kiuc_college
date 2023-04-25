from random import randint

from django.views.generic import TemplateView, FormView
from django.utils.translation import gettext_lazy as _

from apps.feedback.forms import CreateFeedBackForm
from apps.feedback.models import Recaptcha


class ContactsView(TemplateView):
    template_name = 'contacts.html'
