web: gunicorn radio_app.wsgi --log-file -
worker: celery worker -A radio_app --loglevel=info
