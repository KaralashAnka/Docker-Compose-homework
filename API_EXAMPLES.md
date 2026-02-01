# API Примеры запросов

Коллекция примеров для тестирования API системы управления складами.

## Базовый URL
```
http://localhost/api/v1/
```

## Товары (Products)

### 1. Получить список всех товаров
```bash
curl -X GET http://localhost/api/v1/products/
```

### 2. Получить конкретный товар
```bash
curl -X GET http://localhost/api/v1/products/1/
```

### 3. Создать новый товар
```bash
curl -X POST http://localhost/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 15 Pro",
    "description": "Смартфон Apple последнего поколения"
  }'
```

### 4. Обновить товар (полное обновление)
```bash
curl -X PUT http://localhost/api/v1/products/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 15 Pro Max",
    "description": "Обновленное описание"
  }'
```

### 5. Частичное обновление товара
```bash
curl -X PATCH http://localhost/api/v1/products/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 15 Pro Max 256GB"
  }'
```

### 6. Удалить товар
```bash
curl -X DELETE http://localhost/api/v1/products/1/
```

### 7. Поиск товаров по названию
```bash
curl -X GET "http://localhost/api/v1/products/?search=iPhone"
```

### 8. Поиск товаров по описанию
```bash
curl -X GET "http://localhost/api/v1/products/?search=смартфон"
```

## Склады (Stocks)

### 1. Получить список всех складов
```bash
curl -X GET http://localhost/api/v1/stocks/
```

### 2. Получить конкретный склад с товарами
```bash
curl -X GET http://localhost/api/v1/stocks/1/
```

### 3. Создать новый склад без товаров
```bash
curl -X POST http://localhost/api/v1/stocks/ \
  -H "Content-Type: application/json" \
  -d '{
    "address": "г. Екатеринбург, ул. Ленина, 100"
  }'
```

### 4. Создать склад с товарами
```bash
curl -X POST http://localhost/api/v1/stocks/ \
  -H "Content-Type: application/json" \
  -d '{
    "address": "г. Новосибирск, пр. Карла Маркса, 20",
    "positions": [
      {
        "product": 1,
        "quantity": 100,
        "price": "89999.00"
      },
      {
        "product": 2,
        "quantity": 50,
        "price": "8999.00"
      }
    ]
  }'
```

### 5. Обновить склад и его позиции
```bash
curl -X PUT http://localhost/api/v1/stocks/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "address": "г. Москва, ул. Ленина, 10А (обновлено)",
    "positions": [
      {
        "product": 1,
        "quantity": 150,
        "price": "85000.00"
      }
    ]
  }'
```

### 6. Частично обновить склад (только позиции)
```bash
curl -X PATCH http://localhost/api/v1/stocks/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "positions": [
      {
        "product": 1,
        "quantity": 200,
        "price": "89999.00"
      },
      {
        "product": 3,
        "quantity": 75,
        "price": "7999.00"
      }
    ]
  }'
```

### 7. Удалить склад
```bash
curl -X DELETE http://localhost/api/v1/stocks/1/
```

### 8. Найти склады по адресу
```bash
curl -X GET "http://localhost/api/v1/stocks/?search=Москва"
```

### 9. Найти склады с конкретным товаром
```bash
curl -X GET "http://localhost/api/v1/stocks/?products=1"
```

### 10. Найти склады с несколькими товарами
```bash
curl -X GET "http://localhost/api/v1/stocks/?products=1,2,3"
```

## Комплексные сценарии

### Сценарий 1: Добавление нового товара на склад

```bash
# Шаг 1: Создать товар
PRODUCT_ID=$(curl -s -X POST http://localhost/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "MacBook Pro 16",
    "description": "Ноутбук для профессионалов"
  }' | jq -r '.id')

echo "Создан товар с ID: $PRODUCT_ID"

# Шаг 2: Добавить товар на склад
curl -X PATCH http://localhost/api/v1/stocks/1/ \
  -H "Content-Type: application/json" \
  -d "{
    \"positions\": [
      {
        \"product\": $PRODUCT_ID,
        \"quantity\": 25,
        \"price\": \"199999.00\"
      }
    ]
  }"
```

### Сценарий 2: Создание склада с несколькими товарами

```bash
curl -X POST http://localhost/api/v1/stocks/ \
  -H "Content-Type: application/json" \
  -d '{
    "address": "г. Краснодар, ул. Красная, 150",
    "positions": [
      {
        "product": 1,
        "quantity": 30,
        "price": "89999.00"
      },
      {
        "product": 2,
        "quantity": 60,
        "price": "8999.00"
      },
      {
        "product": 3,
        "quantity": 50,
        "price": "7999.00"
      },
      {
        "product": 4,
        "quantity": 20,
        "price": "45999.00"
      }
    ]
  }'
```

### Сценарий 3: Массовый поиск и фильтрация

```bash
# Поиск всех товаров с "Logitech" в названии
curl -X GET "http://localhost/api/v1/products/?search=Logitech"

# Поиск складов в Москве
curl -X GET "http://localhost/api/v1/stocks/?search=Москва"

# Поиск складов с конкретными товарами
curl -X GET "http://localhost/api/v1/stocks/?products=1,2"
```

## Python примеры (requests)

### Создание товара
```python
import requests

url = "http://localhost/api/v1/products/"
data = {
    "title": "Samsung Galaxy S24",
    "description": "Флагманский смартфон Samsung"
}

response = requests.post(url, json=data)
print(response.json())
```

### Получение списка складов
```python
import requests

url = "http://localhost/api/v1/stocks/"
response = requests.get(url)

stocks = response.json()
for stock in stocks['results']:
    print(f"Склад: {stock['address']}")
    print(f"Товаров: {len(stock['positions'])}")
```

### Обновление количества товара
```python
import requests

stock_id = 1
url = f"http://localhost/api/v1/stocks/{stock_id}/"

data = {
    "positions": [
        {
            "product": 1,
            "quantity": 300,
            "price": "89999.00"
        }
    ]
}

response = requests.patch(url, json=data)
print(response.json())
```

## JavaScript примеры (fetch)

### Создание товара
```javascript
const createProduct = async () => {
  const response = await fetch('http://localhost/api/v1/products/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      title: 'iPad Pro',
      description: 'Профессиональный планшет'
    })
  });
  
  const data = await response.json();
  console.log(data);
};

createProduct();
```

### Получение склада
```javascript
const getStock = async (id) => {
  const response = await fetch(`http://localhost/api/v1/stocks/${id}/`);
  const data = await response.json();
  console.log(data);
};

getStock(1);
```

## Postman Collection

Импортируйте эти примеры в Postman:

1. Создайте новую коллекцию "Stocks API"
2. Добавьте переменную окружения `base_url` = `http://localhost/api/v1`
3. Используйте `{{base_url}}` в запросах

## Тестирование

Для тестирования API можно использовать:
- **curl** - из командной строки
- **Postman** - GUI клиент
- **httpie** - улучшенный curl
- **Swagger UI** - встроенная документация на http://localhost/api/v1/docs/

## Примечания

- Все даты возвращаются в формате ISO 8601
- Пагинация работает автоматически (10 элементов на страницу)
- Для фильтрации по нескольким ID используйте запятую: `?products=1,2,3`
- Поиск работает по частичному совпадению (case-insensitive)
