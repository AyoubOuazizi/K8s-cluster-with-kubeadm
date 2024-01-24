from pymongo import MongoClient
from kafka import KafkaProducer
import json
import time
from termcolor import colored
import os

# Définir la variable d'environnement TERM si elle n'est pas déjà définie
if 'TERM' not in os.environ:
    os.environ['TERM'] = 'xterm'  # Vous pouvez également utiliser la valeur appropriée pour votre terminal

def initialize_db():
    # Connexion à la base de données MongoDB
    client_TCP = MongoClient(os.environ.get('MONGO_TCP_URI'))
    client_UDP = MongoClient(os.environ.get('MONGO_UDP_URI'))
    client_ICMP = MongoClient(os.environ.get('MONGO_ICMP_URI'))
    client_UNKNOWN = MongoClient(os.environ.get('MONGO_UNKNOWN_URI'))

    # Sélection de la base de données 'traffic'
    db_TCP = client_TCP['traffic']
    db_UDP = client_UDP['traffic']
    db_ICMP = client_ICMP['traffic']
    db_UNKNOWN = client_UNKNOWN['traffic']

    # Accéder aux collections
    collection_TCP = db_TCP['packets']
    collection_UDP = db_UDP['packets']
    collection_ICMP = db_ICMP['packets']
    collection_UNKNOWN = db_UNKNOWN['packets']

    return {
        'clients': {
            'TCP': client_TCP,
            'UDP': client_UDP,
            'ICMP': client_ICMP,
            'UNKNOWN': client_UNKNOWN
        },
        'collections': {
            'TCP': collection_TCP,
            'UDP': collection_UDP,
            'ICMP': collection_ICMP,
            'UNKNOWN': collection_UNKNOWN
        }
    }

# Connexion à MongoDB
db_info = initialize_db()

# Connexion à Kafka
producer = KafkaProducer(
    bootstrap_servers=os.environ.get('KAFKA_BOOTSTRAP_SERVERS'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Topic Kafka
kafka_topic = os.environ.get('KAFKA_TOPIC')

# Fonction pour calculer les statistiques
def calculate_statistics():
    types = ['TCP', 'UDP', 'ICMP', 'UNKNOWN']
    results = {}
    total_packets_all_types_in_last_second = 0

    for packet_type in types:
        collection = db_info['collections'][packet_type]

        total_packets = collection.count_documents({})
        total_size = sum(packet['packet_size'] for packet in collection.find())

        # Filtrer les paquets dans la dernière seconde avec count_documents
        packets_in_last_second = collection.count_documents({'timestamp': {'$gte': time.time() - 1}})

        results[packet_type] = {
            'total_packets': total_packets,
            'average_size': total_size / total_packets if total_packets else 0,
            'packets_in_last_second': packets_in_last_second
        }

        # Ajouter le nombre total de paquets de ce type au total général
        total_packets_all_types_in_last_second += packets_in_last_second

    # Ajouter le nombre total de paquets de tous les types aux résultats
    results['Total'] = {'total_packets': total_packets_all_types_in_last_second}

    return results

# Boucle infinie pour recalculer en temps réel
while True:
    statistics = calculate_statistics()

    # Effacer l'écran à chaque itération
    os.system('cls' if os.name == 'nt' else 'clear')

    # Affichage coloré dans le terminal
    for packet_type, stats in statistics.items():
        if packet_type != 'Total':  # Exclure le type 'Total' de la boucle
            print(colored(f'{packet_type} Statistics:', 'blue'))
            print(f'Total Packets: {stats["total_packets"]}')

            # Vérifier si la clé 'average_size' existe dans le dictionnaire
            if 'average_size' in stats:
                print(f'Average Size: {stats["average_size"]:.2f}')
            else:
                print('Average Size: N/A')

            print(f'Packets in Last Second: {stats["packets_in_last_second"]}')
            print('-' * 20)

    print(colored(f'General Statistics:', 'blue'))
    print(f'Packets in Last Second: {statistics["Total"]["total_packets"]}')

    # Publier sur Kafka
    producer.send(kafka_topic, value=statistics)

    # Attendre un certain intervalle de temps (par exemple, 1 seconde)
    time.sleep(0.1)