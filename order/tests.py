from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Order, OrderProduct
from datetime import date
# Create your tests here.

class OrderAPITest(APITestCase):

    def setUp(self):
        self.order = Order.objects.create(
            customer_id=1,
            order_date=date.today(),
            total_amount=100.00
        )
        self.order_url = reverse('order-list-create')
        self.order_detail_url = reverse('order-detail', kwargs={'pk': self.order.id})

    def test_create_order(self):
        data = {
            'customer_id': 2,
            'order_date': date.today(),
            'total_amount': 150.00
        }
        response = self.client.post(self.order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_get_order_list(self):
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_detail(self):
        response = self.client.get(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_id'], self.order.customer_id)

    def test_update_order(self):
        data = {
            'customer_id': 1,
            'order_date': date.today(),
            'total_amount': 200.00
        }
        response = self.client.put(self.order_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.total_amount, 200.00)

    def test_delete_order(self):
        response = self.client.delete(self.order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)


class OrderProductAPITest(APITestCase):

    def setUp(self):
        self.order = Order.objects.create(
            customer_id=1,
            order_date=date.today(),
            total_amount=100.00
        )
        self.order_product = OrderProduct.objects.create(
            order_id=self.order.id,
            product_id=10,
            quantity=5
        )
        self.order_product_url = reverse('order-product-list-create')
        self.order_product_detail_url = reverse('order-product-detail', kwargs={'pk': self.order_product.id})

    def test_create_order_product(self):
        data = {
            'order_id': self.order.id,
            'product_id': 11,
            'quantity': 3
        }
        response = self.client.post(self.order_product_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderProduct.objects.count(), 2)

    def test_get_order_product_list(self):
        response = self.client.get(self.order_product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_product_detail(self):
        response = self.client.get(self.order_product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_id'], self.order_product.order_id)

    def test_update_order_product(self):
        data = {
            'order_id': self.order.id,
            'product_id': 10,
            'quantity': 10
        }
        response = self.client.put(self.order_product_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order_product.refresh_from_db()
        self.assertEqual(self.order_product.quantity, 10)

    def test_delete_order_product(self):
        response = self.client.delete(self.order_product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OrderProduct.objects.count(), 0)
