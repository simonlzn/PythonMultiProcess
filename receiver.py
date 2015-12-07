import pika
import json
import multiprocessing

import pipeline

def callback(ch, method, properties, body):
    # load json data
    input_data = json.loads(body)
    
    # message from web server to rabbitMQ
    input_data_key = input_data["key"]
    
    #input_process_id = input_data["id"]
    folder_path = str(input_data["folderPath"])
    input_process_id = str(folder_path.split("/")[-2])+str(folder_path.split("/")[-1])
    
    pipeline_unit = pipeline.Pipeline()
    pipeline_unit.add_process_id(input_process_id)
    pipeline_unit.add_data_key(input_data_key)
    pipeline_unit.add_data(input_data)
    
    process_unit = multiprocessing.Process(target=pipeline_unit.execute())
    process_unit.start()
    

if __name__ == '__main__':    
    # rabittMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    
    channel = connection.channel()
    
    channel.queue_declare(queue='queue3')
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    
    channel.basic_consume(callback, queue='queue3', no_ack=True)
    
    channel.start_consuming()
    