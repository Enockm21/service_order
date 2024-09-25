from rest_framework import serializers
from .models import  Order, OrderProduct

from django.core.cache import cache

class OrderProductSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()


    class Meta:
        model = OrderProduct
        fields = ['product_id', 'quantity', 'product_details',]  # Include product details

    def get_product_details(self, obj):
        # Fetch the available products from cache or global variable
        available_products = cache.get('available_product', [])
        print(available_products,"available_products")
        # Find the detailed product information from the available_products list
        product = next((p for p in available_products if p['id'] == obj.product_id), None)
        
        # Return the product details if found, else return a default message
        if product:
            return {
                'name': product['name'],
                'description': product['description'],
                'price': product['price'],
                'stock': product['stock']
            }
        else:
            return 'Product details not available'

# class OrderProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderProduct
#         fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    # product_ids = serializers.ListField(write_only=True)
    # This field will include the associated products for each order
    products = serializers.SerializerMethodField()
    products_create = OrderProductSerializer(many=True,write_only=True)  # This will accept product data when creating an order

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'order_date', 'total_amount', 'products' ,'products_create']
    def get_products(self, obj):
        # Query the related OrderProduct entries for this orders
        order_products = OrderProduct.objects.filter(order_id=obj.id)
        return OrderProductSerializer(order_products, many=True).data
    def create(self, validated_data):
        # Extract the product data from the validated data
        products_data = validated_data.pop('products_create')
        
        # Create the order
        order = Order.objects.create(**validated_data)

        # Automatically create OrderProduct entries for each product
        for product_data in products_data:
            OrderProduct.objects.create(
                order_id=order.id,  # Link the order ID
                product_id=product_data['product_id'],  # Use the provided product_id
                quantity=product_data['quantity']  # Use the provided quantity
            )

        return order


