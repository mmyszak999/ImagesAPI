db-name=postgres

build:
		docker-compose build

up:
		docker-compose up

fixtures:
		docker-compose exec app_backend bash -c "python3 manage.py loaddata fixtures/fixtures.json"

migrations:
		docker-compose exec app_backend bash -c "python3 manage.py makemigrations && python3 manage.py migrate"

superuser:
		docker-compose exec app_backend bash -c "python3 manage.py createsuperuser"

test:
		docker-compose exec app_backend bash -c "python manage.py test"

backend-bash:
		docker-compose exec app_backend bash

reset-db:
		docker-compose stop app_backend
		docker-compose exec db bash -c "runuser postgres -c 'dropdb $(db-name); createdb $(db-name)'"
		docker-compose start app_backend
		make migrations