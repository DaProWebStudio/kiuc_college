# Деплой / прод-операции

Этот файл — практическая шпаргалка по деплою `college.kiuc.kg` на прод-хост
(`/var/www/kiuc_college`, юзер `kiuc`, supervisor-программа `college`).

Архитектура и общая структура — в корневом `CLAUDE.md`.

---

## Типовой деплой после `git pull`

```bash
cd /var/www/kiuc_college

# 1. Python-зависимости (если pyproject.toml / uv.lock менялись)
uv sync

# 2. Миграции БД
uv run python manage.py migrate

# 3. Переводы — .mo гитигнорятся, всегда пересобираем
uv run python manage.py compilemessages

# 4. CSS — см. раздел ниже (только если меняли шаблоны / input.css)
cd static/build && npm run tw:build && cd -

# 5. Собрать статику для nginx
uv run python manage.py collectstatic --noinput --ignore "build" --ignore "tailwind"

# 6. Перезапуск gunicorn
sudo supervisorctl restart college
```

Если меняли только Python-код (без CSS / шаблонов) — шаги 4–5 можно пропустить.

---

## Сборка `static/css/app.css` (Tailwind v4)

`static/css/app.css` **в `.gitignore`** — это артефакт сборки, в репозитории его нет.
Без него страницы будут без стилей. Чтобы он появился, надо собрать Tailwind.

### Требования

- **Node.js ≥ 20** (Tailwind v4 / `@tailwindcss/oxide` требует именно 20+).
  На Node 18 `npm install` пройдёт с предупреждением `EBADENGINE`, но `npm run tw:build`
  упадёт с `MODULE_NOT_FOUND` для нативного бинарника oxide.

### Первоначальная установка Node 20 на сервере

**Вариант 1 — NodeSource (системно, через apt):**

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
node --version    # v20.x
```

**Вариант 2 — nvm (без sudo, для юзера kiuc):**

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install 20
nvm alias default 20
```

### Сборка

```bash
cd /var/www/kiuc_college/static/build

# Если переходили с Node 18 на 20 — снести старые модули, т.к. oxide
# скомпилирован под версию Node-API конкретной мажорной версии.
rm -rf node_modules package-lock.json

npm install
npm run tw:build         # одноразово, минифицирует → static/css/app.css
# или
npm run tw:watch         # дев-режим, следит за изменениями
```

### Что делает `tw:build`

- Читает `static/tailwind/input.css` (там `@theme`, `@source`, `@layer components`).
- Сканирует `templates/**/*.html` и `apps/**/templates/**/*.html`.
- Пишет минифицированный `static/css/app.css` (~87 KB).

### Кеш-бастинг

Шаблоны грузят CSS как `app.css?{{ style_core_version }}`. После значимых правок CSS
бампь `STYLE_CORE_VERSION` в `.env` (например `v2.1 → v2.2`) и перезапусти gunicorn,
иначе браузеры будут отдавать кэш старой версии.

---

## STATIC_ROOT и collectstatic

- `STATIC_URL = '/static/'`
- Источник: `static/` (`STATICFILES_DIRS`)
- Сборка для прода: `staticfiles/` (`STATIC_ROOT`, гитигнорится)
- nginx раздаёт `/static/` alias → `/var/www/kiuc_college/staticfiles/`

`--ignore "build" --ignore "tailwind"` обязательны: иначе `collectstatic` скопирует
`static/build/node_modules` (десятки мегабайт мусора) и исходник `static/tailwind/input.css`
в `staticfiles/`.

---

## Переводы (i18n)

`.po`-файлы в git, `.mo` — нет.

```bash
# После git pull — пересобрать .mo (обязательно, иначе переводы не подхватятся)
uv run python manage.py compilemessages

# Если добавили новые {% trans %} / gettext в коде / шаблонах:
uv run python manage.py makemessages -l en -l ky --no-location
# отредактировать locale/en|ky/LC_MESSAGES/django.po
uv run python manage.py compilemessages
```

Для translated полей моделей (через `django-modeltranslation`) после добавления
новых полей:

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py update_translation_fields
```

---

## Бэкапы БД

См. `backup.cron` и `scripts/backup_db.sh` в корне репо. Cron-строка ставится через
`sudo crontab -u kiuc -e`. Дампы кладутся в `/var/www/kiuc_college/backups/`,
старше `KEEP_DAYS` (по умолчанию 30) — удаляются автоматически.

Нужен `pg_dump` на PATH (`apt install postgresql-client`).

---

## Supervisor

Конфиг: `config/deploy/college.kiuc.kg.conf` → копируется в `/etc/supervisor/conf.d/`.
Программа называется `college`.

```bash
sudo supervisorctl reread          # перечитать конфиги
sudo supervisorctl update          # применить изменения
sudo supervisorctl restart college # перезапуск после деплоя
sudo supervisorctl status college  # проверить статус
sudo supervisorctl tail -f college stderr   # живые логи
```

Gunicorn биндится на `127.0.0.1:8005`, 2 воркера (см. `gunicorn.conf.py`).
nginx проксирует на этот порт.
