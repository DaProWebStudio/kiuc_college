from django.views.generic import TemplateView, FormView
from django.utils.translation import gettext_lazy as _

from apps.feedback.forms import CreateFeedBackForm
from apps.feedback.models import Recaptcha, FeedBack

from common.utils import get_random_model


class ContactsView(FormView):
    model = FeedBack
    form_class = CreateFeedBackForm
    template_name = 'contacts.html'
    success_url = '/'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recaptcha: Recaptcha = get_random_model(Recaptcha)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recaptcha'] = self.recaptcha
        return context

    def form_valid(self, form):
        form.save(commit=False)
        if int(form.cleaned_data.get('user_answer')) == int(self.recaptcha.answer):
            form.save()
            return super().form_valid(form)
        form.add_error('user_answer', _('Не правильный ответ'))
        return super().form_invalid(form)
