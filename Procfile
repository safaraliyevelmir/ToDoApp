web: gunicorn todoapp_backend.wsgi
worker: celery -A todoapp_backend worker
beat: celery -A todoapp_backend beat -S django