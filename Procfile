web: python manage.py collectstatic --noinput && python manage.py migrate && gunicorn bestia_site.wsgi --log-file -
release: python manage.py migrate --noinput
