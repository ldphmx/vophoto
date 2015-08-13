#Encoding=UTF8

import pymongo
import Config

conn = pymongo.MongoClient(Config.config['mongo_url'])

def get_user(userId, password):
    db = conn.VoiceImageDB
    coll = db.user_profile
    return coll.find_one({'user_id': userId, 'password': password})

def get_user_by_id(userId):
    db = conn.VoiceImageDB
    coll = db.user_profile
    rec = coll.find_one({'user_id': userId})
    return rec;

def register_user(user):
    db = conn.VoiceImageDB
    coll = db.user_profile
    coll.insert_one(user)
    
def get_server_users():
    db = conn.VoiceImageDB
    coll = db.server_usage
    doc = coll.find_one()
    if doc is None:
        servers = Config.config['servers']
        doc = {}
        for server in servers:
            doc[server['name']] = 0
        coll.insert_one(doc)
        
    return doc

def increase_server_usage(server_name, count):
    db = conn.VoiceImageDB
    coll = db.server_usage
    doc = coll.find_one()
    if doc is not None:
        doc[server_name] = doc[server_name] + count
        coll.save(doc)
        
def save_image(image):
    db = conn.VoiceImageDB
    coll = db.voice_images
    coll.save(image)
    
def get_unprocessed(num):
    images = []
    db = conn.VoiceImageDB
    coll = db.voice_images
    unpro = coll.find({'processed': False})
    for doc in unpro:
        images.append(doc)
    
    return images

def save_person(person):
    db = conn.VoiceImageDB
    coll = db.user_facename
    coll.save(person)

