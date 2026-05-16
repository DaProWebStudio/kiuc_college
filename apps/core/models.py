from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from ckeditor.fields import RichTextField

from common.utils import get_english_translit as get_slug
from common.upload_to_files import (
    document_files,
    cooperation_files,
    international_images,
    international_main_img,
    edu_process_files,
    international_pdf
)
from common.managers import ActiveManager
from common import constants as cons


class Cooperation(models.Model):
    """Сотрудничество"""
    title = models.CharField(_("Название"), max_length=255)
    file = models.FileField(_("Файл"), validators=[FileExtensionValidator(['pdf'])], upload_to=cooperation_files)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Сотрудничество')
        verbose_name_plural = _('Сотрудничество')


class InternationalCooperation(models.Model):
    """Международное сотрудничество"""
    title = models.CharField(_('Название'), max_length=230)
    slug = models.SlugField("URL", max_length=255, null=True, blank=True)
    description = RichTextField(_('Описание'), blank=True, null=True)
    image = ProcessedImageField(verbose_name=_('Фото'), upload_to=international_main_img, format='webp',
                                processors=[ResizeToFill(2268, 1296)], options={'quality': 90})

    file = models.FileField(_("Договор (PDF)"), validators=[FileExtensionValidator(['pdf'])],
                            upload_to=international_pdf, null=True, blank=True)

    objects = models.Manager()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.title)
        super(InternationalCooperation, self).save(*args, **kwargs)

    def get_absolute_url(self, **kwargs):
        return reverse('international_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Международное сотрудничество')
        verbose_name_plural = _('Международные сотрудничество')


class InternationalCooperationImages(models.Model):
    """Фотографии Международное сотрудничество"""
    international = models.ForeignKey(InternationalCooperation, on_delete=models.CASCADE, related_name='images')
    image = ProcessedImageField(verbose_name=_('Фотография'), upload_to=international_images, format='webp', options={'quality': 80})

    def __str__(self):
        return str(self.international.title)

    class Meta:
        verbose_name = _('Фотография')
        verbose_name_plural = _('Фотографии')


class Document(models.Model):
    title = models.CharField(_("Название"), max_length=255)
    is_active = models.BooleanField(_("Активный"), default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Нормативный документ')
        verbose_name_plural = _('Нормативные документы')


class DocumentFile(models.Model):
    document = models.ForeignKey(Document, verbose_name=_("Документ"), on_delete=models.CASCADE, related_name='files')
    title = models.CharField(_("Название файла"), max_length=255)
    file = models.FileField(
        _("Файл"), validators=[FileExtensionValidator(['pdf', 'png', 'jpg', 'webp'])], upload_to=document_files
    )

    def __str__(self):
        return f'{self.document} - {self.title}'

    class Meta:
        verbose_name = _('Файл документа')
        verbose_name_plural = _('Файлы документа')


class EduProcess(models.Model):
    title = models.CharField(_("Название"), max_length=255)
    is_active = models.BooleanField(_("Активный"), default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Учебный процесс')
        verbose_name_plural = _('Учебные процессы')


class EduProcessFile(models.Model):
    process = models.ForeignKey(EduProcess, verbose_name=_("Документ"), on_delete=models.CASCADE, related_name='files')
    title = models.CharField(_("Название файла"), max_length=255)
    file = models.FileField(
        _("Файл"), validators=[FileExtensionValidator(['pdf', 'png', 'jpg', 'webp'])], upload_to=edu_process_files
    )

    def __str__(self):
        return f'{self.process} - {self.title}'

    class Meta:
        verbose_name = _('Файл учебного процесса')
        verbose_name_plural = _('Файлы учебных процессов')


RECEPTION_DEFAULT_BODY = """\
<p>Кыргызский международный универсальный колледж рад пригласить Вас в наше учебное заведение. Наш колледж предоставляет широкую возможность выбора специальностей, приносящих успех и стабильный доход в различных сферах деятельности.</p>

<p>Образовательный процесс в колледже организуют квалифицированные преподаватели. Колледж располагает оборудованными кабинетами и компьютерными классами. Мы поддерживаем тесные контакты с зарубежными партнёрами — есть возможность обучения в одном из лучших вузов Республики Корея.</p>

<h5>Срок обучения</h5>
<ul>
  <li><strong>На базе 9 класса</strong> — 2 года 10 месяцев</li>
  <li><strong>На базе 11 класса</strong> — 1 год 10 месяцев</li>
</ul>

<h5>Условия приёма</h5>
<p>Колледж принимает выпускников 9, 10 и 11 классов. Чтобы поступить, абитуриентам достаточно оставить заявку и предоставить аттестат об окончании 9 или 11 классов. Конкурсный отбор первокурсников проводится по среднему баллу аттестата.</p>

<h5>Основной список документов</h5>
<ul>
  <li>Оригинал аттестата и свидетельства об образовании</li>
  <li>Медицинская справка №086-У</li>
  <li>Свидетельство о рождении или паспорт (копия)</li>
  <li>Фотографии 3×4 (6 штук)</li>
  <li>Скоросшиватель и конверт</li>
</ul>

<h5>Подача документов</h5>
<p>Подайте документы онлайн через информационную систему колледжа или посетите лично приёмную комиссию по адресу: Сокулукский район, г. Шопоков, ул. Машиностроительная, 13а.</p>
<p>Списки рекомендованных к зачислению составляются по убыванию среднего балла аттестата. Будьте на связи в последний день тура.</p>

<h5>Как считается средний балл аттестата</h5>
<p>Подсчитайте общее количество оценок, сложите все оценки вместе и разделите эту сумму на общее количество оценок. Полученное число и будет средним баллом Вашего аттестата (с точностью до сотых долей).</p>

<blockquote>
<strong>Пример.</strong> В аттестате 12 предметов: 5 пятёрок, 3 четвёрки и 4 тройки.<br>
5×5 + 4×3 + 3×4 = 25 + 12 + 12 = 49 → 49 ÷ 12 = <strong>4.08</strong>
</blockquote>
"""


class ReceptionPage(models.Model):
    """Singleton-страница «Абитуриентам». В админке всегда ровно одна запись —
    редактор колледжа может править hero / lead / основной текст и сайдбар-контакты."""

    heading = models.CharField(
        _('Заголовок'), max_length=240,
        default='Уважаемые <i>абитуриенты!</i>',
        help_text=_('Можно вставить HTML — например, оберни слово в '
                    '&lt;i&gt;...&lt;/i&gt; чтобы выделить курсивом.'),
    )
    lead = models.TextField(
        _('Подзаголовок'),
        default='Кыргызский международный универсальный колледж ждёт Вас. '
                'Программы среднего профессионального образования, международные стажировки.',
    )
    body = RichTextField(_('Основной текст'), blank=True, default=RECEPTION_DEFAULT_BODY)

    contacts_title = models.CharField(_('Заголовок контактов'), max_length=120, default='Контакты приёмной')
    contact_phone = models.CharField(_('Телефон'), max_length=40, blank=True, default='+996 (706) 95-56-77')
    contact_whatsapp = models.CharField(_('WhatsApp (номер)'), max_length=40, blank=True, default='+996 (706) 95-56-77')
    contact_email = models.EmailField(_('Email'), blank=True, default='info@college.kiuc.kg')
    contact_website_label = models.CharField(_('Подпись сайта'), max_length=120, blank=True, default='2020.edu.gov.kg')
    contact_website_url = models.URLField(
        _('Ссылка на сайт'), blank=True,
        default='https://2020.edu.gov.kg/spuz/reports?id_university=168',
    )

    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(_('Страница «Абитуриентам»'))

    def save(self, *args, **kwargs):
        # Singleton: всегда pk=1; вторая запись схлопывается в update первой.
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Singleton нельзя удалить через ORM.
        pass

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name = _('Страница «Абитуриентам»')
        verbose_name_plural = _('Страница «Абитуриентам»')


class AbstractResume(models.Model):
    GENDER_CHOICES = (
        (cons.MEN, _('Мужской')),
        (cons.WOMEN, _('Женский'))
    )

    number = models.IntegerField(_('Порядковый номер'), null=True, blank=True, default=100)
    last_name = models.CharField(_('Фамилия'), max_length=50)
    first_name = models.CharField(_('Имя'), max_length=50)
    sur_name = models.CharField(_('Отчество'), max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    gender = models.CharField(_('Пол'), max_length=10, choices=GENDER_CHOICES, default=cons.MEN)
    date_of_birth = models.DateField(_('День рождения'))
    description = RichTextField(verbose_name='Резюме')
    email = models.EmailField('Email', blank=True, null=True)
    instagram = models.URLField('instagram', blank=True, null=True)
    facebook = models.URLField('facebook', blank=True, null=True)

    is_active = models.BooleanField("Активный", default=True)

    objects = models.Manager()
    active = ActiveManager()

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def get_full_name(self):
        """ Полное имя """
        if self.sur_name:
            return f'{self.last_name} {self.first_name} {self.sur_name}'
        return f'{self.last_name} {self.first_name}'

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.get_full_name())
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.sur_name if self.sur_name else ""}'