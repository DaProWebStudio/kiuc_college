from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _

from apps.feedback.forms import CreateFeedBackForm
from apps.feedback.models import Recaptcha, FeedBack

from common.utils import get_random_model


class ContactsView(FormView):
    model = FeedBack
    form_class = CreateFeedBackForm
    template_name = 'contacts.html'
    success_url = reverse_lazy('contacts')

    def get_recaptcha(self) -> Recaptcha | None:
        if not hasattr(self, '_recaptcha'):
            # POST сверяет ответ с той капчей, что показали на GET, а не с новой случайной
            pk = self.request.session.get('recaptcha_id') if self.request.method == 'POST' else None
            self._recaptcha = Recaptcha.objects.filter(pk=pk).first() if pk else None
            if self._recaptcha is None:
                self._recaptcha = get_random_model(Recaptcha)
            if self._recaptcha is not None:
                self.request.session['recaptcha_id'] = self._recaptcha.pk
        return self._recaptcha

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # без капчи поле ответа не выводится — значит, и не обязательно
        form.fields['user_answer'].required = self.get_recaptcha() is not None
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recaptcha'] = self.get_recaptcha()
        return context

    def form_valid(self, form):
        recaptcha = self.get_recaptcha()
        if recaptcha is not None and int(form.cleaned_data.get('user_answer')) != int(recaptcha.answer):
            form.add_error('user_answer', _('Не правильный ответ'))
            return self.form_invalid(form)
        form.save()
        messages.success(self.request, _('Спасибо! Ваше сообщение отправлено — мы свяжемся с вами в ближайшее время.'))
        return super().form_valid(form)
