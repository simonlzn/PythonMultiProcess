import pika
import time
import json

from send import *
from worker import *
from multiprocessing import Process

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='itk',
                   queue=queue_name)

print(' [*] Waiting for messages. To exit press CTRL+C')

def new1(self, queue_name, key):
	sender = Sender()
	sender.send('{\"key\":\"' + key + '\"}')

	connection = pika.BlockingConnection(pika.ConnectionParameters(
		host='localhost'))
	channel = connection.channel()
	channel.queue_declare(queue_name)
	channel.queue_bind(exchange='itk',
		       queue=queue_name,
		       routing_key=queue_name)

	channel.basic_consume(callback1,
			      queue=queue_name,
			      no_ack=True)
	channel.start_consuming()

def callback1(ch, method, properties, body):
	sender = Sender()
	data = json.loads(body)
	sender.send('{\"key\":\"' + data["key"] + '\"}')

	print body
def callback(ch, method, properties, body):
    data = json.loads(body)
    worker = Worker()
    p = Process(target=new1, args=(data["id"], data["key"],))
    p.start()
    '''
    sender = Sender()
    sender.send("{ \"key\":\"" + data["key"] + "\"}")
    '''

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()   
