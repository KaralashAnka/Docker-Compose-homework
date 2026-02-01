from django_filters import rest_framework as filters
from .models import Product, Stock


class ProductFilter(filters.FilterSet):
    """Фильтр для товаров"""
    title = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Product
        fields = ['title', 'description']


class StockFilter(filters.FilterSet):
    """Фильтр для складов"""
    products = filters.CharFilter(method='filter_products')
    
    class Meta:
        model = Stock
        fields = ['address']
    
    def filter_products(self, queryset, name, value):
        """Фильтр складов по ID товаров (через запятую)"""
        if not value:
            return queryset
        
        product_ids = [int(id.strip()) for id in value.split(',') if id.strip().isdigit()]
        
        if product_ids:
            return queryset.filter(products__id__in=product_ids).distinct()
        
        return queryset
