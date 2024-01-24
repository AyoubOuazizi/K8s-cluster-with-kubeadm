import os
import pyshark
from confluent_kafka import Producer
import json
import time
import configparser

# Obtenir le chemin absolu du répertoire du script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Charger la configuration depuis config.ini dans le même répertoire que le script
config_file_path = os.path.join(script_directory, 'config.ini')
config = configparser.ConfigParser()
config.read(config_file_path)

# Kafka configuration
producer_config = {
    'bootstrap.servers': config['Kafka']['bootstrap_servers'],
    'client.id': 'packet-producer'
}
kafka_topic = config['Kafka']['topic']

# Network configuration
network_interface = config['Network']['interface']

# Create a Kafka producer instance
producer = Producer(producer_config)

# Create a capture object for the desired network device
cap = pyshark.LiveCapture(interface=network_interface)

# Define a callback function to process each captured packet
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

    # Display all packet information
    print(pkt)

    # Publish the JSON data to the Kafka topic
    producer.produce(kafka_topic, value=json_data)

    # Flush the producer's message queue to ensure delivery
    producer.flush()

# Start real-time capture
try:
    cap.apply_on_packets(packet_handler)
except KeyboardInterrupt:
    print("Fin du programme")
finally:
    # Close the Kafka producer
    producer.flush()
    # producer.close()