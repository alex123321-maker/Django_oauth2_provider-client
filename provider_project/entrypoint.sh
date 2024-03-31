#!/bin/sh

# Ожидание доступности базы данных
echo "Waiting for database to be available..."
# (Здесь может быть ваш код для проверки доступности БД, например, для PostgreSQL)

# Применение миграций
echo "Applying database migrations..."
python manage.py migrate

# Создание суперпользователя
echo "Creating superuser..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@example.com', 'root')"

# Сбор статических файлов
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Запуск Gunicorn
echo "Starting Gunicorn..."
exec gunicorn provider_project.wsgi:application --bind 0.0.0.0:8000 --log-level info
