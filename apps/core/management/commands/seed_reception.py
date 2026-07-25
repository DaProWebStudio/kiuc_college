"""Английская и кыргызская версии страницы «Абитуриентам».

Текст страницы лежит в БД (ReceptionPage), а modeltranslation при создании
записи копирует русский default во все языки — поэтому на /en/ и /ky/ она
показывалась по-русски. Команда дозаполняет переводы и идемпотентна:
поле трогается, только если оно всё ещё совпадает с русским, то есть
редактор колледжа его не правил.
"""
from django.core.management.base import BaseCommand

from apps.core.models import ReceptionPage, RECEPTION_DEFAULT_BODY

BODY_EN = """\
<p>The Kyrgyz International Universal College is glad to invite you to our institution. The college offers a wide choice of specialties that bring success and a stable income in many fields of work.</p>

<p>Teaching is delivered by qualified lecturers. The college has well-equipped classrooms and computer labs. We keep close ties with partners abroad — there is an opportunity to study at one of the leading universities of the Republic of Korea.</p>

<h5>Duration of study</h5>
<ul>
  <li><strong>After grade 9</strong> — 2 years 10 months</li>
  <li><strong>After grade 11</strong> — 1 year 10 months</li>
</ul>

<h5>Admission requirements</h5>
<p>The college admits graduates of grades 9, 10 and 11. To apply, it is enough to submit an application and provide the certificate of completion of grade 9 or 11. First-year students are selected competitively, by the grade point average of the certificate.</p>

<h5>Documents required</h5>
<ul>
  <li>Original school certificate and education diploma</li>
  <li>Medical certificate No. 086-U</li>
  <li>Birth certificate or passport (copy)</li>
  <li>Photographs 3×4 (6 pieces)</li>
  <li>A document folder and an envelope</li>
</ul>

<h5>Submitting documents</h5>
<p>Submit your documents online through the college information system, or come to the admissions office in person at: Sokuluk district, Shopokov, 13a Mashinostroitelnaya street.</p>
<p>Lists of applicants recommended for enrolment are drawn up in descending order of the certificate grade point average. Stay reachable on the final day of the round.</p>

<h5>How the grade point average is calculated</h5>
<p>Count the total number of marks, add all the marks together and divide that sum by the total number of marks. The result is the grade point average of your certificate, to two decimal places.</p>

<blockquote>
<strong>Example.</strong> The certificate lists 12 subjects: five 5s, three 4s and four 3s.<br>
5×5 + 4×3 + 3×4 = 25 + 12 + 12 = 49 → 49 ÷ 12 = <strong>4.08</strong>
</blockquote>
"""

BODY_KY = """\
<p>Кыргыз эл аралык универсалдуу колледжи Сизди окуу жайыбызга чакырууга кубанычта. Колледжибиз ар кандай тармактарда ийгилик жана туруктуу киреше алып келүүчү адистиктердин кеңири тандоосун сунуштайт.</p>

<p>Колледжде окуу процессин квалификациялуу окутуучулар уюштурат. Колледжде жабдылган кабинеттер жана компьютердик класстар бар. Биз чет өлкөлүк өнөктөштөр менен тыгыз байланышта иштейбиз — Корея Республикасынын мыкты жогорку окуу жайларынын биринде окууга мүмкүнчүлүк бар.</p>

<h5>Окуу мөөнөтү</h5>
<ul>
  <li><strong>9-класстын базасында</strong> — 2 жыл 10 ай</li>
  <li><strong>11-класстын базасында</strong> — 1 жыл 10 ай</li>
</ul>

<h5>Кабыл алуу шарттары</h5>
<p>Колледж 9, 10 жана 11-класстын бүтүрүүчүлөрүн кабыл алат. Тапшыруу үчүн арыз калтыруу жана 9 же 11-классты бүткөндүгү жөнүндө аттестатты тапшыруу жетиштүү. Биринчи курска конкурстук тандоо аттестаттын орточо баллы боюнча жүргүзүлөт.</p>

<h5>Документтердин негизги тизмеси</h5>
<ul>
  <li>Аттестаттын жана билими жөнүндө күбөлүктүн түп нускасы</li>
  <li>№086-У медициналык маалымкат</li>
  <li>Туулгандыгы жөнүндө күбөлүк же паспорт (көчүрмөсү)</li>
  <li>3×4 сүрөт (6 даана)</li>
  <li>Папка жана конверт</li>
</ul>

<h5>Документтерди тапшыруу</h5>
<p>Документтерди колледждин маалыматтык системасы аркылуу онлайн тапшырыңыз же кабыл алуу комиссиясына өзүңүз келиңиз: Сокулук району, Шопоков шаары, Машиностроительная көчөсү, 13а.</p>
<p>Кабыл алууга сунушталгандардын тизмеси аттестаттын орточо баллынын кемүү тартибинде түзүлөт. Турдун акыркы күнү байланышта болуңуз.</p>

<h5>Аттестаттын орточо баллы кантип эсептелет</h5>
<p>Бааларыңыздын жалпы санын эсептеңиз, бардык бааларды кошуп, чыккан сумманы баалардын жалпы санына бөлүңүз. Чыккан сан — Сиздин аттестатыңыздын орточо баллы (жүздүк үлүшкө чейинки тактык менен).</p>

<blockquote>
<strong>Мисал.</strong> Аттестатта 12 предмет бар: 5 бештик, 3 төрттүк жана 4 үчтүк.<br>
5×5 + 4×3 + 3×4 = 25 + 12 + 12 = 49 → 49 ÷ 12 = <strong>4.08</strong>
</blockquote>
"""

TRANSLATIONS = {
    'heading': {
        'en': 'Dear <i>applicants!</i>',
        'ky': 'Урматтуу <i>абитуриенттер!</i>',
    },
    'lead': {
        'en': 'The Kyrgyz International Universal College is waiting for you. Vocational secondary-education '
              'programmes and international internships.',
        'ky': 'Кыргыз эл аралык универсалдуу колледжи Сизди күтөт. Кесиптик орто билим берүү программалары, '
              'эл аралык стажировкалар.',
    },
    'contacts_title': {
        'en': 'Admissions office contacts',
        'ky': 'Кабыл алуу бөлүмүнүн байланыштары',
    },
    'body': {
        'en': BODY_EN,
        'ky': BODY_KY,
    },
}


class Command(BaseCommand):
    help = 'Заполняет английскую и кыргызскую версии страницы «Абитуриентам».'

    def handle(self, *args, **options):
        page = ReceptionPage.load()
        filled, skipped = [], []

        for field, by_language in TRANSLATIONS.items():
            russian = getattr(page, f'{field}_ru') or ''
            # Тело правил редактор колледжа — свой текст переводить нам нечем.
            if field == 'body' and russian.strip() != RECEPTION_DEFAULT_BODY.strip():
                skipped.append(field)
                continue
            for language, value in by_language.items():
                current = getattr(page, f'{field}_{language}') or ''
                if current and current != russian:
                    skipped.append(f'{field}_{language}')
                    continue
                setattr(page, f'{field}_{language}', value)
                filled.append(f'{field}_{language}')

        if filled:
            page.save()
            self.stdout.write(self.style.SUCCESS(f'Заполнено полей: {len(filled)} — {", ".join(filled)}'))
        else:
            self.stdout.write('Всё уже переведено — пропускаю.')
        if skipped:
            self.stdout.write(f'Не тронуто (правил редактор): {", ".join(skipped)}')
