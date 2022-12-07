web: gunicorn project.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate
web: python website/manage.py runserver theguru.herokuapp.com
