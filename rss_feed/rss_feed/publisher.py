# In the name of GOD
import pika
from datetime import datetime

class Publisher:
    def __init__(self) :
        self.connection_parameter = pika.ConnectionParameters('localhost')


    def publish(self, message, queue) :
        self.connection = pika.BlockingConnection(self.connection_parameter)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(exchange='', routing_key=queue, body='success' + message)
        print(f'{message} Published Successfully! at {datetime.now()}')
        self.connection.close()

    def error_publish(self, message, queue) :
        self.connection = pika.BlockingConnection(self.connection_parameter)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(exchange='', routing_key=queue, body='error!!' + message)
        print(f'{message} Published Successfully! at {datetime.now()}')
        self.connection.close()
