run-server:
	docker-compose up -d
	python manage.py migrate
	python manage.py runserver

delete-db:
	rm -f db.sqlite3

run-tests:
	python manage.py test --settings=application.settings --keepdb -v 2
