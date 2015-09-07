'''
Created on Sep 7, 2015

@author: v-shayi
'''
import pickle
import pymongo
import os.path
from src import Config
from src import Utils
import bmemcached

mc = bmemcached.Client((Config.config['memcached_host'],))

if __name__ == '__main__':
    user_id = '127f46fc-f21e-4911-a734-be4abfa8b318' #modify later for specific user
    conn = pymongo.MongoClient(Config.config['mongo_url'])
    db = conn.VoiceImageDB
    coll = db.voice_images
    docs = coll.find()
    
    indexer = [[], []]
    imgs = []
    
    for doc in docs:
#         indexer[0].append(doc['time'])
#         indexer[1].append(doc['image_name'])
        imgs.append(doc)
        
    sorted_indexer = sorted(imgs, key=lambda img: img['time'])
    
    for index in sorted_indexer:
        indexer[0].append(index['time'])
        indexer[1].append(index['image_name'])
        
    filename = Utils.get_user_path(user_id) + "/" + "time_indexer.dat"
    if not os.path.isfile(filename):
        os.remove(filename)
     
    with open(filename,'wb') as fp:
        pickle.dump(indexer,fp)
    fp.close()
         
    with open(filename,'rb') as fp:
            indexer_read = pickle.load(fp)
    
    mc.set(user_id, indexer_read)
    fp.close()
    
    print(indexer_read[0])
    print(indexer_read[1])
    print(len(indexer_read[1]))