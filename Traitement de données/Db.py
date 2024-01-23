from pymongo import MongoClient

def initialize_db() :
    # Connexion à la base de données MongoDB
    client_TCP = MongoClient('mongodb://localhost:27017/') 
    client_UDP = MongoClient('mongodb://localhost:27018/') 
    client_ICMP = MongoClient('mongodb://localhost:27019/') 
    client_UNKNOWN = MongoClient('mongodb://localhost:27020/') 

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