#!/bin/bash

export DJANGO_ADMIN_URL="admin"
export DATABASE_URL="mysql://django-RAAGo:tenuki-forever@localhost:3306/RAAGo"
#export DJANGO_SETTINGS_MODULE=config.settings.production
#export DJANGO_SECRET_KEY=jklasdlkjsadjlasdlas
#export DJANGO_AWS_ACCESS_KEY_ID=jaskdjsakdjaskd
#export DJANGO_AWS_SECRET_ACCESS_KEY=aaaasdqwewdsds
#export DJANGO_AWS_STORAGE_BUCKET_NAME=pqopwqopieqwopeqwope
#export DJANGO_MAILGUN_API_KEY=aasalkdaslkdlasdqwjeqjwkej
#export DJANGO_MAILGUN_SERVER_NAME=RAAGo-mailserver
#export DJANGO_ALLOWED_HOSTS=elsantodel90.tk:8000
#export DJANGO_ALLOWED_HOSTS="rango.elsantodel90.tk"
#export DJANGO_ALLOWED_HOSTS=localhost
 ./manage.py $@ runserver 0.0.0.0:8000
#gunicorn -b 0.0.0.0 --worker-connection 8 $@ config.wsgi:application
