import pika

class ExternalQueue:
    def sendMessage(config_data):
        connection = pika.BlockingConnection(pika.ConnectionParameters('coqueue', 5672, '/', pika.PlainCredentials('root', 'root123')))
        channel = connection.channel()

        channel.basic_publish(exchange='co_topic', routing_key='', body=str(config_data))
        
        connection.close()

    def sendMessage(data, key):
        connection = pika.BlockingConnection(pika.ConnectionParameters('coqueue', 5672, '/', pika.PlainCredentials('root', 'root123')))
        channel = connection.channel()
        channel.basic_publish(exchange='co_topic', routing_key=key, body=str(data))
        
        connection.close()
if __name__ == "__main__":
    d = '{"_id": {"$oid": "6040e6e2457fbd3fbea6faef"}, "name": "ngnix_orch", "state": "queue", "node_mapping": "node0", "image": "ngnix", "last_state_update_time": {"$date": 1614866146839}, "service_map": "orch"}'
    import json
    ExternalQueue.sendMessage(data=d, key="co_node_12375")