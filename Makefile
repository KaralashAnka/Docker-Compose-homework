.PHONY: help build up down restart logs shell migrate makemigrations createsuperuser test collectstatic loaddata clean

help:
	@echo "Доступные команды:"
	@echo "  make build          - Собрать Docker образы"
	@echo "  make up             - Запустить контейнеры"
	@echo "  make down           - Остановить контейнеры"
	@echo "  make restart        - Перезапустить контейнеры"
	@echo "  make logs           - Показать логи всех сервисов"
	@echo "  make shell          - Открыть Django shell"
	@echo "  make migrate        - Применить миграции"
	@echo "  make makemigrations - Создать миграции"
	@echo "  make createsuperuser - Создать суперпользователя"
	@echo "  make test           - Запустить тесты"
	@echo "  make collectstatic  - Собрать статические файлы"
	@echo "  make loaddata       - Загрузить тестовые данные"
	@echo "  make clean          - Остановить и удалить все контейнеры и volumes"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-postgres:
	docker-compose logs -f postgres

logs-nginx:
	docker-compose logs -f nginx

shell:
	docker-compose exec backend python manage.py shell

bash:
	docker-compose exec backend bash

migrate:
	docker-compose exec backend python manage.py migrate

makemigrations:
	docker-compose exec backend python manage.py makemigrations

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

test:
	docker-compose exec backend python manage.py test

collectstatic:
	docker-compose exec backend python manage.py collectstatic --noinput

loaddata:
	docker-compose exec backend python manage.py loaddata fixtures/initial_data.json

clean:
	docker-compose down -v
	docker system prune -f

psql:
	docker-compose exec postgres psql -U stocks_user -d stocks_db

backup-db:
	docker-compose exec postgres pg_dump -U stocks_user stocks_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db:
	@read -p "Введите имя файла backup: " backup_file; \
	docker-compose exec -T postgres psql -U stocks_user stocks_db < $$backup_file

install:
	@echo "Установка проекта..."
	cp .env.example .env
	@echo "Отредактируйте файл .env и установите свои значения"
	@echo "Затем выполните: make build && make up && make migrate && make createsuperuser"
