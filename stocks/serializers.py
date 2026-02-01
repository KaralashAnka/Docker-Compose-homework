from rest_framework import serializers
from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товара"""
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class StockProductSerializer(serializers.ModelSerializer):
    """Сериализатор для позиции товара на складе"""
    
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockProductDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для позиции товара на складе"""
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = StockProduct
        fields = ['id', 'product', 'quantity', 'price', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class StockSerializer(serializers.ModelSerializer):
    """Сериализатор для склада"""
    positions = StockProductSerializer(many=True, required=False)
    
    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        """Создание склада с позициями"""
        positions_data = validated_data.pop('positions', [])
        stock = Stock.objects.create(**validated_data)
        
        for position_data in positions_data:
            StockProduct.objects.create(stock=stock, **position_data)
        
        return stock
    
    def update(self, instance, validated_data):
        """Обновление склада с позициями"""
        positions_data = validated_data.pop('positions', None)
        
        # Обновляем поля склада
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        
        # Обновляем позиции, если они переданы
        if positions_data is not None:
            # Получаем список product_id из новых позиций
            new_products = {pos['product'].id for pos in positions_data}
            
            # Удаляем позиции, которых нет в новом списке
            instance.positions.exclude(product_id__in=new_products).delete()
            
            # Создаем или обновляем позиции
            for position_data in positions_data:
                StockProduct.objects.update_or_create(
                    stock=instance,
                    product=position_data['product'],
                    defaults={
                        'quantity': position_data['quantity'],
                        'price': position_data['price']
                    }
                )
        
        return instance


class StockDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор для склада с полной информацией о товарах"""
    positions = StockProductDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
