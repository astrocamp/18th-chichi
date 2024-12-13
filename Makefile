.PHONY: server
server:
	poetry run python manage.py runserver


.PHONY: migrations
migrations:
	poetry run python manage.py makemigrations


.PHONY: migrate
migrate:
	poetry run python manage.py migrate

.PHONY: shell
shell:
	poetry run python manage.py shell_plus

.PHONY: precommit
precommit:
	poetry run pre-commit

.PHONY: commit
commit:
	poetry run cz commit
