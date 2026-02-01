from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, Stock, StockProduct


class ProductModelTest(TestCase):
    """Тесты модели Product"""
    
    def setUp(self):
        self.product = Product.objects.create(
            title='Тестовый товар',
            description='Описание тестового товара'
        )
    
    def test_product_creation(self):
        """Тест создания товара"""
        self.assertEqual(self.product.title, 'Тестовый товар')
        self.assertIsNotNone(self.product.created_at)
    
    def test_product_str(self):
        """Тест строкового представления товара"""
        self.assertEqual(str(self.product), 'Тестовый товар')


class StockModelTest(TestCase):
    """Тесты модели Stock"""
    
    def setUp(self):
        self.stock = Stock.objects.create(address='г. Москва, ул. Ленина, 1')
        self.product = Product.objects.create(title='Товар')
        StockProduct.objects.create(
            stock=self.stock,
            product=self.product,
            quantity=10,
            price=100.00
        )
    
    def test_stock_creation(self):
        """Тест создания склада"""
        self.assertEqual(self.stock.address, 'г. Москва, ул. Ленина, 1')
    
    def test_stock_products(self):
        """Тест связи склада с товарами"""
        self.assertEqual(self.stock.products.count(), 1)


class ProductAPITest(APITestCase):
    """Тесты API для товаров"""
    
    def setUp(self):
        self.product_data = {
            'title': 'API Товар',
            'description': 'Описание API товара'
        }
    
    def test_create_product(self):
        """Тест создания товара через API"""
        response = self.client.post('/api/v1/products/', self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().title, 'API Товар')
    
    def test_get_products_list(self):
        """Тест получения списка товаров"""
        Product.objects.create(**self.product_data)
        response = self.client.get('/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_product_detail(self):
        """Тест получения детальной информации о товаре"""
        product = Product.objects.create(**self.product_data)
        response = self.client.get(f'/api/v1/products/{product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Товар')
    
    def test_update_product(self):
        """Тест обновления товара"""
        product = Product.objects.create(**self.product_data)
        updated_data = {'title': 'Обновленный товар', 'description': 'Новое описание'}
        response = self.client.put(f'/api/v1/products/{product.id}/', updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.title, 'Обновленный товар')
    
    def test_delete_product(self):
        """Тест удаления товара"""
        product = Product.objects.create(**self.product_data)
        response = self.client.delete(f'/api/v1/products/{product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)


class StockAPITest(APITestCase):
    """Тесты API для складов"""
    
    def setUp(self):
        self.product1 = Product.objects.create(title='Товар 1')
        self.product2 = Product.objects.create(title='Товар 2')
        self.stock_data = {
            'address': 'г. Москва, ул. Ленина, 10',
            'positions': [
                {
                    'product': self.product1.id,
                    'quantity': 50,
                    'price': '1000.00'
                },
                {
                    'product': self.product2.id,
                    'quantity': 30,
                    'price': '1500.00'
                }
            ]
        }
    
    def test_create_stock(self):
        """Тест создания склада с позициями"""
        response = self.client.post('/api/v1/stocks/', self.stock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Stock.objects.count(), 1)
        stock = Stock.objects.first()
        self.assertEqual(stock.positions.count(), 2)
    
    def test_get_stocks_list(self):
        """Тест получения списка складов"""
        self.client.post('/api/v1/stocks/', self.stock_data, format='json')
        response = self.client.get('/api/v1/stocks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_filter_stocks_by_product(self):
        """Тест фильтрации складов по товару"""
        self.client.post('/api/v1/stocks/', self.stock_data, format='json')
        response = self.client.get(f'/api/v1/stocks/?products={self.product1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_search_products(self):
        """Тест поиска товаров"""
        Product.objects.create(title='Ноутбук', description='Игровой')
        response = self.client.get('/api/v1/products/?search=ноутбук')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
