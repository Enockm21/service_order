import pika
import json
import threading
from django.core.cache import cache

# Global variable to store products
available_products = []

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
def start_consumer_thread():
    thread = threading.Thread(target=consume_products)
    thread.daemon = True  # Daemonize thread to run in background
    thread.start()



# import pika
# import json

# def publish_order_created(order_data):
#     connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
#     channel = connection.channel()

#     # Declare exchange
#     channel.exchange_declare(exchange='service_exchange', exchange_type='topic')

#     # Publish a message to the exchange
#     message = json.dumps(order_data)
#     channel.basic_publish(
#         exchange='service_exchange',
#         routing_key='order.created',  # Topic key for order created event
#         body=message
#     )

#     print("Order created message published")
#     connection.close()

# if __name__ == "__main__":
#     order_data = {
#         'order_id': 123,
#         'client_id': 456,
#         'product_ids': [1, 2, 3]
#     }
#     publish_order_created(order_data)
