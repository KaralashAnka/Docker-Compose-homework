from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Stock
from .serializers import (
    ProductSerializer,
    StockSerializer,
    StockDetailSerializer
)
from .filters import ProductFilter, StockFilter


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с товарами.
    
    list: Получить список всех товаров
    create: Создать новый товар
    retrieve: Получить конкретный товар
    update: Обновить товар
    partial_update: Частично обновить товар
    destroy: Удалить товар
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']


class StockViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы со складами.
    
    list: Получить список всех складов
    create: Создать новый склад
    retrieve: Получить конкретный склад
    update: Обновить склад
    partial_update: Частично обновить склад
    destroy: Удалить склад
    """
    queryset = Stock.objects.all().prefetch_related('positions__product')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = StockFilter
    search_fields = ['address']
    ordering_fields = ['created_at', 'address']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'retrieve':
            return StockDetailSerializer
        return StockSerializer
