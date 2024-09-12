from django.apps import AppConfig
from .service_order import start_consumer_thread  # Import the consumer

class OrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "order"
    def ready(self):
        # Start the RabbitMQ consumer in a separate thread when Django starts
        start_consumer_thread()
    
