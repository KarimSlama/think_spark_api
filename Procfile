web: python manage.py migrate && gunicorn project.wsgi
worker: daphne project.asgi:application --port $PORT --bind 0.0.0.0