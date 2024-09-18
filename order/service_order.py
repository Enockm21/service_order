import pika
import json
import threading
from django.core.cache import cache
import os
import django
from decimal import Decimal

# Global variable to store products
available_products = []


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

# Then use this encoder when calling json.dumps()

def callback(ch, method, properties, body):
    global available_products
    product_data = json.loads(body)
    available_products = product_data['products']
    cache.set('available_product', available_products, timeout=None)
    print(f"Received product list: {available_products}")

def consume_products():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare exchange and queue for product list
    channel.exchange_declare(exchange='product_exchange', exchange_type='topic')
    channel.queue_declare(queue='order_service_product_queue')

    # Bind the queue to the exchange with routing key 'product.list'
    channel.queue_bind(exchange='product_exchange', queue='order_service_product_queue', routing_key='product.list')

    # Start consuming product list
    channel.basic_consume(queue='order_service_product_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for product list...')
    channel.start_consuming()

# Start the consumer in a separate thread


def callback(ch, method, properties, body):
    data = json.loads(body)
    print(data)  # Add this line to see what the data looks like
    customer_id = data.get('customer_id')  # Use .get() to avoid KeyError if key is missing
    if not customer_id:
        print("Error: 'customer_id' is missing from the message.")
        return

    # Fetch the orders for the given customer_id
    from order.models import Order
    orders = Order.objects.filter(customer_id=customer_id)
    
    # Prepare the list of orders as a response
    order_list = [{
        'order_id': order.id,
        'total_amount': order.total_amount,
        'order_date': order.order_date.strftime('%Y-%m-%d')
    } for order in orders]

    # Publish the response back to RabbitMQ (to a different queue or exchange)
    publish_order_response(customer_id, order_list)

def consume_order_requests():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the exchange and queue for order requests
    channel.exchange_declare(exchange='order_exchange', exchange_type='topic')
    channel.queue_declare(queue='order_service_queue')

    # Bind the queue to the exchange with routing key 'customer.order.request'
    channel.queue_bind(exchange='order_exchange', queue='order_service_queue', routing_key='customer.order.request')

    # Start consuming order requests
    channel.basic_consume(queue='order_service_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for order requests...')
    channel.start_consuming()

def publish_order_response(customer_id, orders):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Convert Decimal fields to float
    for order in orders:
        if isinstance(order['total_amount'], Decimal):
            order['total_amount'] = float(order['total_amount'])

    # Prepare the response message
    message = {
        'customer_id': customer_id,
        'orders': orders
    }
    body = json.dumps(message, cls=DecimalEncoder)
    print(message,"message")
    # Publish the response back to RabbitMQ
    channel.basic_publish(
        exchange='order_response_exchange',
        routing_key=f'customer.{customer_id}.order.response',
        body=json.dumps(message)
    )

    print(f"Published order response for customer {customer_id}")
    connection.close()

def start_consumer_thread():
    #thread consumer
    thread = threading.Thread(target=consume_products)
    thread.daemon = True  # Daemonize thread to run in background
    thread.start()
    #thread order
    thread_customer = threading.Thread(target=consume_order_requests)
    thread_customer.daemon = True 
    thread_customer.start()
