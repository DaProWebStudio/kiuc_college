"""Первичное наполнение контактов колледжа.

Запускается один раз после миграции, добавившей SiteContact: русские значения
приходят из default'ов модели, а команда дозаполняет en/ky и список менеджеров
приёмной комиссии — раньше они были захардкожены в шаблонах и .po-файлах.
Идемпотентна: уже заполненные поля не трогает.
"""
from django.core.management.base import BaseCommand

from apps.core.models import SiteContact, ContactPerson

TRANSLATIONS = {
    'address_short': {
        'en': 'Shopokov, 25a Mashinostroitelnaya st.',
        'ky': 'Шопоков ш., Машиностроительная көч., 25а',
    },
    'address_full': {
        'en': 'Chui region, Sokuluk district, Shopokov, 25a Mashinostroitelnaya str.',
        'ky': 'Чуй обл., Сокулук р., Шопоков, көч. Машиностроительная, 25а',
    },
    'street_address': {
        'en': '25a Mashinostroitelnaya str.',
        'ky': 'Машиностроительная көч., 25а',
    },
    'locality': {
        'en': 'Shopokov',
        'ky': 'Шопоков',
    },
    'region': {
        'en': 'Sokuluk district, Chui region',
        'ky': 'Сокулук району, Чуй облусу',
    },
}

MANAGERS = [
    {
        'number': 1,
        'phone': '+996 (704) 25-50-80',
        'full_name': 'Сууханкул кызы Акмарал',
        'full_name_en': 'Suukhankul kyzy Akmaral',
        'full_name_ky': 'Сууханкул кызы Акмарал',
    },
    {
        'number': 2,
        'phone': '+996 (700) 02-22-51',
        'full_name': 'Сыздыкова Айгерим Рысбековна',
        'full_name_en': 'Syzdykova Aigerim Rysbekovna',
        'full_name_ky': 'Сыздыкова Айгерим Рысбековна',
    },
    {
        'number': 3,
        'phone': '+996 (706) 16-66-68',
        'full_name': 'Абдыкеримова Аниса Меймановна',
        'full_name_en': 'Abdykerimova Anisa Meimanovna',
        'full_name_ky': 'Абдыкеримова Аниса Меймановна',
    },
]


class Command(BaseCommand):
    help = 'Создаёт запись контактов колледжа и заполняет её значениями по умолчанию.'

    def handle(self, *args, **options):
        contact = SiteContact.load()

        # modeltranslation копирует default в колонку каждого языка, поэтому
        # «непереведённым» считаем поле, которое пустое или равно русскому.
        filled = []
        for field, by_language in TRANSLATIONS.items():
            russian = getattr(contact, f'{field}_ru')
            for language, value in by_language.items():
                current = getattr(contact, f'{field}_{language}')
                if not current or current == russian:
                    setattr(contact, f'{field}_{language}', value)
                    filled.append(f'{field}_{language}')
        if filled:
            contact.save()
            self.stdout.write(self.style.SUCCESS(f'Заполнено переводов: {len(filled)}'))
        else:
            self.stdout.write('Переводы уже заполнены — пропускаю.')

        if contact.managers.exists():
            self.stdout.write('Менеджеры уже заведены — пропускаю.')
            return

        ContactPerson.objects.bulk_create([ContactPerson(contact=contact, **data) for data in MANAGERS])
        self.stdout.write(self.style.SUCCESS(f'Добавлено менеджеров: {len(MANAGERS)}'))
