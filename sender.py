import pika

class Sender(object):
    def send(self, message):
        credentials = pika.PlainCredentials('sphic', 'sphic')
        #connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.11.12.33', credentials= credentials))
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        
        channel.exchange_declare(exchange='java',type='fanout')
        
        channel.queue_declare(queue='queue1',durable=True) 
        
        channel.basic_publish(exchange='java', routing_key='queue1', body=message)
        
        print("[x] Sent "+message)
        
        connection.close()
