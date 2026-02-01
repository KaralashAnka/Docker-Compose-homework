# Система управления складами и запасами

Проект представляет собой REST API для управления складами, товарами и их запасами, развернутый с использованием Docker Compose.

## 📋 Описание

Веб-приложение на Django REST Framework для учета товаров на складах:
- Управление товарами (создание, редактирование, удаление)
- Управление складами
- Учет остатков товаров на складах
- Поиск и фильтрация товаров

## 🏗️ Архитектура

Проект состоит из трех контейнеров:
- **Backend** - Django приложение с Gunicorn
- **PostgreSQL** - база данных
- **Nginx** - веб-сервер и reverse proxy

## 🚀 Быстрый старт

### Предварительные требования

- Docker (версия 20.10+)
- Docker Compose (версия 2.0+)

### Установка и запуск

1. **Клонируйте репозиторий:**
```bash
git clone <your-repo-url>
cd stocks_project
```

2. **Создайте файл .env:**
```bash
cp .env.example .env
```

Отредактируйте `.env` и установите свои значения:
```env
DEBUG=False
SECRET_KEY=your-very-secret-key-change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=stocks_db
POSTGRES_USER=stocks_user
POSTGRES_PASSWORD=secure_password_here
DB_HOST=postgres
DB_PORT=5432
```

3. **Соберите и запустите контейнеры:**
```bash
docker-compose up -d --build
```

4. **Выполните миграции:**
```bash
docker-compose exec backend python manage.py migrate
```

5. **Создайте суперпользователя:**
```bash
docker-compose exec backend python manage.py createsuperuser
```

6. **Загрузите тестовые данные (опционально):**
```bash
docker-compose exec backend python manage.py loaddata fixtures/initial_data.json
```

## 🌐 Доступ к приложению

После успешного запуска:
- **API**: http://localhost/api/v1/
- **Admin панель**: http://localhost/admin/
- **API документация**: http://localhost/api/v1/docs/

## 📚 API Endpoints

### Товары (Products)

- `GET /api/v1/products/` - Список всех товаров
- `POST /api/v1/products/` - Создать товар
- `GET /api/v1/products/{id}/` - Получить товар
- `PUT /api/v1/products/{id}/` - Обновить товар
- `PATCH /api/v1/products/{id}/` - Частично обновить товар
- `DELETE /api/v1/products/{id}/` - Удалить товар

**Фильтрация:**
- `?search=название` - поиск по названию и описанию
- `?price_min=100` - минимальная цена
- `?price_max=1000` - максимальная цена

### Склады (Stocks)

- `GET /api/v1/stocks/` - Список всех складов
- `POST /api/v1/stocks/` - Создать склад
- `GET /api/v1/stocks/{id}/` - Получить склад
- `PUT /api/v1/stocks/{id}/` - Обновить склад
- `PATCH /api/v1/stocks/{id}/` - Частично обновить склад
- `DELETE /api/v1/stocks/{id}/` - Удалить склад

**Фильтрация:**
- `?search=название` - поиск по названию и адресу
- `?products=1,2,3` - склады с определенными товарами

## 📝 Примеры использования API

### Создание товара

```bash
curl -X POST http://localhost/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ноутбук",
    "description": "Игровой ноутбук"
  }'
```

### Создание склада с позициями

```bash
curl -X POST http://localhost/api/v1/stocks/ \
  -H "Content-Type: application/json" \
  -d '{
    "address": "г. Москва, ул. Ленина, 10",
    "positions": [
      {
        "product": 1,
        "quantity": 50,
        "price": 75000
      },
      {
        "product": 2,
        "quantity": 30,
        "price": 1500
      }
    ]
  }'
```

### Обновление количества товара на складе

```bash
curl -X PATCH http://localhost/api/v1/stocks/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "positions": [
      {
        "product": 1,
        "quantity": 100,
        "price": 75000
      }
    ]
  }'
```

### Поиск товаров

```bash
# Поиск по названию
curl "http://localhost/api/v1/products/?search=ноутбук"

# Фильтр по цене
curl "http://localhost/api/v1/products/?price_min=1000&price_max=5000"
```

### Поиск складов с товаром

```bash
curl "http://localhost/api/v1/stocks/?products=1"
```

## 🛠️ Команды управления

### Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f nginx
```

### Выполнение команд Django

```bash
# Миграции
docker-compose exec backend python manage.py migrate

# Создание миграций
docker-compose exec backend python manage.py makemigrations

# Сбор статики
docker-compose exec backend python manage.py collectstatic --noinput

# Shell
docker-compose exec backend python manage.py shell

# Запуск тестов
docker-compose exec backend python manage.py test
```

### Работа с базой данных

```bash
# Подключение к PostgreSQL
docker-compose exec postgres psql -U stocks_user -d stocks_db

# Backup базы данных
docker-compose exec postgres pg_dump -U stocks_user stocks_db > backup.sql

# Restore базы данных
docker-compose exec -T postgres psql -U stocks_user stocks_db < backup.sql
```

### Остановка и удаление

```bash
# Остановка контейнеров
docker-compose down

# Остановка с удалением volumes (БД будет удалена!)
docker-compose down -v

# Пересборка после изменений
docker-compose up -d --build
```

## 🧪 Тестирование

Запуск тестов:

```bash
docker-compose exec backend python manage.py test
```

Запуск с покрытием:

```bash
docker-compose exec backend coverage run --source='.' manage.py test
docker-compose exec backend coverage report
```

## 📂 Структура проекта

```
stocks_project/
├── docker-compose.yml          # Конфигурация Docker Compose
├── Dockerfile                  # Dockerfile для backend
├── requirements.txt            # Python зависимости
├── .env.example               # Пример переменных окружения
├── .dockerignore              # Исключения для Docker
├── README.md                  # Документация
├── nginx/
│   └── nginx.conf             # Конфигурация Nginx
├── stocks_products/           # Основной Django проект
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── stocks/                    # Django приложение
│   ├── models.py              # Модели данных
│   ├── serializers.py         # Сериализаторы DRF
│   ├── views.py               # API views
│   ├── urls.py                # URL маршруты
│   ├── admin.py               # Admin панель
│   └── tests.py               # Тесты
├── fixtures/                  # Тестовые данные
│   └── initial_data.json
└── manage.py                  # Django manage скрипт
```

## 🔧 Разработка

### Локальная разработка без Docker

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте PostgreSQL локально и обновите `.env`

4. Запустите миграции:
```bash
python manage.py migrate
```

5. Запустите сервер разработки:
```bash
python manage.py runserver
```

### Добавление новых зависимостей

1. Добавьте пакет в `requirements.txt`
2. Пересоберите контейнер:
```bash
docker-compose up -d --build backend
```

## 🐛 Решение проблем

### Контейнеры не запускаются

```bash
# Проверьте логи
docker-compose logs

# Проверьте статус
docker-compose ps

# Пересоздайте контейнеры
docker-compose down
docker-compose up -d --build
```

### Ошибка подключения к БД

```bash
# Проверьте, что PostgreSQL запущен
docker-compose ps postgres

# Проверьте логи PostgreSQL
docker-compose logs postgres

# Проверьте переменные окружения
docker-compose exec backend env | grep POSTGRES
```

### Проблемы со статикой

```bash
# Пересоберите статику
docker-compose exec backend python manage.py collectstatic --noinput

# Перезапустите nginx
docker-compose restart nginx
```

### Порт 80 уже занят

Измените порт в `docker-compose.yml`:
```yaml
nginx:
  ports:
    - "8080:80"  # Используйте 8080 вместо 80
```

## 📊 Модели данных

### Product (Товар)
- `id` - ID товара
- `title` - Название
- `description` - Описание

### Stock (Склад)
- `id` - ID склада
- `address` - Адрес
- `positions` - Связь с товарами через StockProduct

### StockProduct (Позиция на складе)
- `stock` - Ссылка на склад
- `product` - Ссылка на товар
- `quantity` - Количество
- `price` - Цена

## 🔐 Безопасность

- Измените `SECRET_KEY` в production
- Используйте сильные пароли для БД
- Настройте `ALLOWED_HOSTS` правильно
- Не коммитьте `.env` файл в git
- Используйте HTTPS в production

## 📄 Лицензия

MIT License

## 👨‍💻 Автор

Создано для курса Netology по Django

## 🤝 Содействие

Pull requests приветствуются. Для крупных изменений сначала откройте issue для обсуждения.

## 📞 Поддержка

Если у вас возникли проблемы, создайте issue в репозитории проекта.
