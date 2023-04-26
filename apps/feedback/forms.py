from django.forms import ModelForm, Textarea, TextInput, EmailInput, IntegerField, NumberInput
from django.utils.translation import gettext_lazy as _

from .models import FeedBack


class CreateFeedBackForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['required'] = 'required'

    user_answer = IntegerField(widget=NumberInput(attrs={'class': 'input', 'placeholder': _('Напишите ответ')}))

    class Meta:
        model = FeedBack
        fields = ['name', 'email', 'message', 'user_answer']
        widgets = {
            'name': TextInput(attrs={
                'class': 'input',
                "placeholder": _("Ваше имя"),
                "minlength": "3",
                "maxlength": "25",
            }),
            'email': EmailInput(attrs={
                'class': 'input',
                "placeholder": _("Ваша электронная почта"),
            }),
            'message': Textarea(attrs={
                'class': 'message',
                "placeholder": _("Ваше сообщение"),
                "minlength": "20",
                "maxlength": "5000",
            }),
        }
