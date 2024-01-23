from confluent_kafka import Consumer, KafkaError
from Db import *
import json

# Configuration du consommateur Kafka
consumer_config = {
    'bootstrap.servers': 'localhost:29092',  # les serveurs Kafka
    'group.id': 'packet-consumer',
    'auto.offset.reset': 'earliest'  # Réinitialisation de l'offset au début du topic en cas de consommateur nouveau
}

# Création d'une instance de consommateur Kafka
consumer = Consumer(consumer_config)

# Abonnement au topic "capture"
kafka_topic = 'capture'
consumer.subscribe([kafka_topic])

# Configuration de MongoDB
db_info = initialize_db()
clients = db_info['clients']
collections = db_info['collections']

# Boucle de consommation des messages
try:
    while True:
        msg = consumer.poll(0)  # Attente minimale pour de nouveaux messages
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        message_data = json.loads(msg.value().decode('utf-8'))
        print('Received message: ', message_data)
        insert_into_mongodb(collections, message_data)
except KeyboardInterrupt:
    pass
finally:
    # Fermeture du consommateur Kafka
    consumer.close()
    close_db(clients)