from django.contrib import admin

from apps.feedback.models import FeedBack, Recaptcha


@admin.register(FeedBack)
class AdminFeedBack(admin.ModelAdmin):
    """ Обратная связь """
    list_display = ('name', 'email', 'created')


@admin.register(Recaptcha)
class AdminRecaptcha(admin.ModelAdmin):
    """ ReCaptcha """
    list_display = ('answer', 'created', 'updated')