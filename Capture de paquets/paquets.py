import pyshark
from confluent_kafka import Producer
import json
import time

# Create a Kafka producer configuration
producer_config = {
    'bootstrap.servers': '35.226.86.80:32531',  # Replace with your Kafka bootstrap servers
    # 'bootstrap.servers': '34.42.176.246:9092',  # Replace with your Kafka bootstrap servers
    'client.id': 'packet-producer'
}

# Create a Kafka producer instance
producer = Producer(producer_config)

# Define the Kafka topic
kafka_topic = 'capture'

# Créez un objet de capture pour le périphérique réseau souhaité
cap = pyshark.LiveCapture(interface="Wi-Fi" )

# Définissez une fonction de rappel pour traiter chaque paquet capturé
def packet_handler(pkt):
    packet_data = {}

    if "eth" in pkt:
        packet_data['src_mac'] = pkt.eth.src
        packet_data['dst_mac'] = pkt.eth.dst

    if "ip" in pkt:
        packet_data['src_ip'] = pkt.ip.src
        packet_data['dst_ip'] = pkt.ip.dst

    packet_data['packet_type'] = pkt.transport_layer if hasattr(pkt, 'transport_layer') else 'Unknown'

    packet_data['packet_size'] = len(pkt)

    packet_data['timestamp'] = time.time()

    # Convert packet data to JSON
    json_data = json.dumps(packet_data)

    # Affichez toutes les informations du paquet
    print(pkt)

    # Publish the JSON data to the Kafka topic
    producer.produce(kafka_topic, value=json_data)

    # Flush the producer's message queue to ensure delivery
    producer.flush()

# Démarrez la capture en temps réel
try:
    cap.apply_on_packets(packet_handler)
except KeyboardInterrupt:
    print("Fin du programme")
finally:
    # Close the Kafka producer
    producer.flush()
    # producer.close()
