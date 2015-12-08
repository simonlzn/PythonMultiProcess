import pika

class Sender(object):
    def send(self, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        
        channel.exchange_declare(exchange='java')
        
        channel.queue_declare(queue='queue1',durable=True) 
        
        channel.basic_publish(exchange='java', routing_key='queue1', body=message)
        
        print("[x] Sent "+message)
        
        connection.close()
