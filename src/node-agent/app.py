import pika
connection = pika.BlockingConnection(pika.ConnectionParameters('coqueue', 5672, '/', pika.PlainCredentials("root", "root123")))
channel = connection.channel()

def callback(ch, method, properties, body):
    print(dir(body))
    print(f'{body}  are received')
    
channel.basic_consume(queue="node2", on_message_callback=callback, auto_ack=True)
channel.start_consuming()