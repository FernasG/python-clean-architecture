run:
	python3 manage.py runserver
test:
	python3 manage.py test
migrate:
	python3 manage.py migrate
.PHONY: all test clean