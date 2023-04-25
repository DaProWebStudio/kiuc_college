from random import randint

from django.views.generic import TemplateView, FormView
from django.utils.translation import gettext_lazy as _

from apps.feedback.forms import CreateFeedBackForm
from apps.feedback.models import Recaptcha, FeedBack


class ContactsView(FormView):
    model = FeedBack
    form_class = CreateFeedBackForm
    template_name = 'contacts.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recaptcha'] = Recaptcha.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
