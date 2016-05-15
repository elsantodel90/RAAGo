web: gunicorn config.wsgi:application
worker: celery worker --app=aago_ranking.taskapp --loglevel=info
