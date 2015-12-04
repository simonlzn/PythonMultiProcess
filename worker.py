import pika
from send import *

class Worker(object):

    def new(self, queue_name, key):
	sender = Sender()
	sender.send('{\"key\":\"' + key + '\"}')

	connection = pika.BlockingConnection(pika.ConnectionParameters(
        	host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue_name)
	channel.queue_bind(exchange='itk',
                       queue=queue_name,
                       routing_key=queue_name)
	
	channel.basic_consume(self.callback,
        	              queue=queue_name,
                	      no_ack=True)
	channel.start_consuming()

    def callback(ch, method, properties, body):
	sender = Sender()
	data = json.loads(body)
	sender.send('{\"key\":\"' + data["key"] + '\"}')

	print body
