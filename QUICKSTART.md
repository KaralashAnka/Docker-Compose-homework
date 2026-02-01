# Быстрый старт проекта

## 🚀 Установка за 5 минут

### 1. Подготовка окружения

```bash
# Клонируйте проект
git clone <your-repo>
cd stocks_project

# Создайте .env файл
cp .env.example .env

# Отредактируйте .env (измените SECRET_KEY и пароли!)
nano .env
```

### 2. Запуск проекта

```bash
# Сборка и запуск контейнеров
docker-compose up -d --build

# Выполнение миграций
docker-compose exec backend python manage.py migrate

# Создание суперпользователя
docker-compose exec backend python manage.py createsuperuser

# Загрузка тестовых данных (опционально)
docker-compose exec backend python manage.py loaddata fixtures/initial_data.json
```

### 3. Готово! 🎉

Откройте в браузере:
- API: http://localhost/api/v1/
- Admin: http://localhost/admin/
- Документация: http://localhost/api/v1/docs/

## 📝 Основные команды

```bash
# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Тесты
docker-compose exec backend python manage.py test
```

## 🔧 С Makefile (если установлен make)

```bash
make build          # Сборка
make up             # Запуск
make migrate        # Миграции
make createsuperuser # Создать суперпользователя
make loaddata       # Загрузить тестовые данные
make logs           # Логи
make test           # Тесты
```

## 📚 Примеры API запросов

### Создать товар
```bash
curl -X POST http://localhost/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Новый товар", "description": "Описание"}'
```

### Получить список товаров
```bash
curl http://localhost/api/v1/products/
```

### Создать склад с товарами
```bash
curl -X POST http://localhost/api/v1/stocks/ \
  -H "Content-Type: application/json" \
  -d '{
    "address": "г. Москва, ул. Пушкина, 1",
    "positions": [
      {"product": 1, "quantity": 100, "price": "1000.00"}
    ]
  }'
```

## ❓ Проблемы?

1. **Порт 80 занят?** Измените в docker-compose.yml:
   ```yaml
   nginx:
     ports:
       - "8080:80"  # Используйте 8080
   ```

2. **Контейнеры не запускаются?**
   ```bash
   docker-compose logs
   docker-compose down -v
   docker-compose up -d --build
   ```

3. **Ошибка подключения к БД?**
   ```bash
   docker-compose logs postgres
   # Проверьте переменные в .env
   ```

## 📖 Полная документация

См. [README.md](README.md) для детальной информации.
