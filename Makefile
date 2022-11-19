db-name=postgres
fixture-files = fixtures/fixtures.json

build:
		docker-compose build

up:		
		docker-compose up	

load-fixtures:
		docker-compose exec app_backend bash -c "python3 manage.py loaddata $(fixture-files)"

migrations:
		docker-compose exec app_backend bash -c "python3 manage.py makemigrations api && python3 manage.py migrate"

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