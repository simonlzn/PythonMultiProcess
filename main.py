import pika
import json
import sys
import os
import multiprocessing
import sender
import pipeline

def callback(ch, method, properties, body):
    # load json data
    input_data = json.loads(body)
    
    process_id = str(input_data["id"])
    input_data_key = str(input_data["key"])
    
    print(body)
    #print(dictionary)
    
    senders = sender.Sender()
    senders.send('{\"key\":\"' + input_data_key + '\"}')
    
    if process_id in dictionary:
        return
    else: 
        process_unit = multiprocessing.Process(target=new_process, args=(process_id,input_data_key,body,))
        process_unit.start()
        dictionary.add(process_id)
    
def new_process(queue_name,key, body):
    sys.stdout = open(str(os.getpid())+'.out','a')
    print("new process")
    #senders = sender.Sender()
    #senders.send('{\"key\":\"' + key + '\"}')
    credentials = pika.PlainCredentials('sphic', 'sphic')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.11.12.33', credentials= credentials))
    
    global pipeline_unit
    pipeline_unit = pipeline.Pipeline()
    
    input_data = json.loads(body)
    input_data_id = str(input_data["id"])
    input_data_key = str(input_data["key"])
    pipeline_unit.set_process_id(input_data_id)
    pipeline_unit.set_data(input_data)
    pipeline_unit.set_data_key(input_data_key)
    pipeline_unit.execute()
    
    channel = connection.channel()
    
    queue_unit = channel.queue_declare(exclusive=True)
    queue_unit_name = queue_unit.method.queue
    
    channel.queue_bind(exchange='itk',queue=queue_unit_name,routing_key=queue_name)
    
    channel.basic_consume(new_process_callback, queue=queue_unit_name, no_ack=True)
    
    sys.stdout.flush()
    
    channel.start_consuming()
    
def new_process_callback(ch, method, properties, body):
    sys.stdout = open(str(os.getpid())+".out","a")
    print("new process callback")
    
    #senders = sender.Sender()
    
    input_data = json.loads(body)
    input_data_id = str(input_data["id"])
    input_data_key = str(input_data["key"])
    
    
    #print("id= ",input_data_id)
    #senders.send('{\"key\":\"' + input_data_key + '\",\"data\":\"'+str(input_data)+'\"}')
    
    #print(pipeline_unit)
    
    #if not 'pipeline_unit' in globals():
    #    pipeline_unit = pipeline.Pipeline()
    
    sys.stdout.flush()
    
    pipeline_unit.set_process_id(input_data_id)
    pipeline_unit.set_data(input_data)
    pipeline_unit.set_data_key(input_data_key)
    pipeline_unit.execute()
    
    sys.stdout.flush()


if __name__ == '__main__':   
    credentials = pika.PlainCredentials('sphic', 'sphic')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.11.12.33', credentials= credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange='itk', type='topic', durable=False)
    queue_unit = channel.queue_declare(exclusive=True)
    queue_name = queue_unit.method.queue
    
    channel.queue_bind(exchange='itk', queue=queue_name, routing_key='#')
    
    global dictionary
    dictionary = set()
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    
    channel.start_consuming()
    
    
    