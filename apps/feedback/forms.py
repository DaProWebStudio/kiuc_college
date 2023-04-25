from django.forms import ModelForm, Textarea, TextInput, EmailInput
from django.utils.translation import gettext_lazy as _

from .models import FeedBack


class CreateFeedBackForm(ModelForm):
    class Meta:
        model = FeedBack
        fields = ['name', 'email', 'message']
        widgets = {
            'name': TextInput(attrs={
                'class': 'input',
                "placeholder": _("Ваше имя"),
                "minlength": "3",
                "maxlength": "25",
                "required": "required"
            }),
            'email': EmailInput(attrs={
                'class': 'input',
                "placeholder": _("Ваша электронная почта"),
                "required": "required"
            }),
            'message': Textarea(attrs={
                'class': 'message',
                "placeholder": _("Ваше сообщение"),
                "minlength": "20",
                "maxlength": "5000",
                "required": "required"
            }),
        }
