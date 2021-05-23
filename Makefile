install:
    pipenv install --dev

activate:
	pipenv shell

run:
	python manage.py runserver

migration:
	python manage.py makemigrations

migrate:
 	python manage.py migrate

cov:
	coverage run --source='.' manage.py test

test:
	python manage.py test --keepdb

test-unit:
	python manage.py test --keepdb --patterns="*_spec.py"


