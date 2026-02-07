# Belts Django Project

## Быстрый запуск 

1. Запуск бд :

```bash
docker compose up -d
```

3. Устанавливаем зависимости:

```bash
pip install -r requirements.txt
```

4. Запускаем миграции:

```bash
python manage.py migrate
```

5. Запускаем Django сервер:

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: `http://127.0.0.1:8000/`.

## Конфиг

- Eнв должен храниться в `belts/config/.env`.
