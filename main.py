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
    
    print("***")
    print(dictionary)
    
    if process_id in dictionary:
        return
    else: 
        process_unit = multiprocessing.Process(target=new_process, args=(process_id,input_data_key,))
        process_unit.start()
        dictionary.add(process_id)
    
def new_process(queue_name,key):
    sys.stdout = open(str(os.getpid())+'.out','a')
    print("new process")
    senders = sender.Sender()
    senders.send('{\"key\":\"' + key + '\"}')
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    #pipeline_unit = pipeline.Pipeline()
    
    global pipeline_unit
    pipeline_unit = pipeline.Pipeline()
    
    #print(pipeline_unit)
    print("xxx")
    
    channel = connection.channel()
    channel.queue_declare(queue_name)
    channel.queue_bind(exchange='itk',queue=queue_name,routing_key=queue_name)
    
    channel.basic_consume(new_process_callback, queue=queue_name, no_ack=True)
    
    channel.start_consuming()
    
def new_process_callback(ch, method, properties, body):
    sys.stdout = open(str(os.getpid())+".out","a")
    print("new process callback")
    
    #senders = sender.Sender()
    
    input_data = json.loads(body)
    input_data_id = str(input_data["id"])
    input_data_key = str(input_data["key"])
    
    print("!!!")
    print(input_data)
    
    #print("id= ",input_data_id)
    #senders.send('{\"key\":\"' + input_data_key + '\"}')
    
    #print(pipeline_unit)
    
    #if not 'pipeline_unit' in globals():
    #    pipeline_unit = pipeline.Pipeline()
       
    pipeline_unit.set_process_id(input_data_id)
    pipeline_unit.set_data(input_data)
    pipeline_unit.set_data_key(input_data_key)
    pipeline_unit.exectue()
    
    


if __name__ == '__main__':   
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
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
    
    
    