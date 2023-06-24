run:
	docker-compose up -d
	python manage.py migrate
	python manage.py runserver
