web: python manage.py collectstatic --noinput && gunicorn bestia_site.wsgi --log-file -
release: python manage.py migrate --noinput
