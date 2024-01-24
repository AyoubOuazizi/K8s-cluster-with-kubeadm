from pymongo import MongoClient
import os

def initialize_db() :
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

def insert_into_mongodb(collections, data) :
    if data['packet_type'] == "TCP":
        collections['TCP'].insert_one(data)
    elif data['packet_type'] == "UDP":
        collections['UDP'].insert_one(data)
    elif data['packet_type'] == "ICMP":
        collections['ICMP'].insert_one(data)
    else:
        collections['UNKNOWN'].insert_one(data)

def close_db(clients) :
    for client in clients.values() :
        client.close()