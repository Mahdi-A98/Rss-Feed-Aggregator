# In the name of GOD
import pika
from datetime import datetime
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rss_feed.settings')
django.setup()

from django.conf import settings
class Publisher:
    def __init__(self) :
        self.connection_parameter = pika.ConnectionParameters(settings.RABBITMQ_HOST)


    def publish(self, message, queue) :
        self.connection = pika.BlockingConnection(self.connection_parameter)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(exchange='', routing_key=queue, body='success' + message)
        self.connection.close()

    def error_publish(self, message, queue) :
        self.connection = pika.BlockingConnection(self.connection_parameter)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(exchange='', routing_key=queue, body='error!!' + message)
        self.connection.close()
