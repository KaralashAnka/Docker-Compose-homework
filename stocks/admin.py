from django.contrib import admin
from .models import Product, Stock, StockProduct


class StockProductInline(admin.TabularInline):
    """Inline для позиций товаров на складе"""
    model = StockProduct
    extra = 1
    fields = ['product', 'quantity', 'price']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка для товаров"""
    list_display = ['id', 'title', 'description', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'description']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """Админка для складов"""
    list_display = ['id', 'address', 'get_products_count', 'created_at', 'updated_at']
    list_display_links = ['id', 'address']
    search_fields = ['address']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [StockProductInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('address',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_products_count(self, obj):
        """Количество товаров на складе"""
        return obj.products.count()
    
    get_products_count.short_description = 'Количество товаров'


@admin.register(StockProduct)
class StockProductAdmin(admin.ModelAdmin):
    """Админка для позиций товаров на складах"""
    list_display = ['id', 'stock', 'product', 'quantity', 'price', 'created_at']
    list_display_links = ['id']
    list_filter = ['stock', 'created_at']
    search_fields = ['stock__address', 'product__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('stock', 'product', 'quantity', 'price')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
