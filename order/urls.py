from django.urls import path
from .views import OrderListCreate, OrderRetrieveUpdateDestroy, OrderProductListCreate, OrderProductRetrieveUpdateDestroy



urlpatterns = [   
    path('orders/', OrderListCreate.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroy.as_view(), name='order-detail'),
    path('order-products/', OrderProductListCreate.as_view(), name='order-product-list-create'),
    path('order-products/<int:pk>/', OrderProductRetrieveUpdateDestroy.as_view(), name='order-product-detail'),
]

