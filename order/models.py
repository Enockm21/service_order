from django.db import models

# Create your models here.
class Order(models.Model):
    customer_id = models.IntegerField()
    order_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} - Customer {self.customer_id}"

class OrderProduct(models.Model):
    order_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        unique_together = (('order_id', 'product_id'),)
    
    def __str__(self):
        return f"Order {self.order_id} - Product {self.product_id}"
