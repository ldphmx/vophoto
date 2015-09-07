'''
Created on Sep 7, 2015

@author: v-shayi
'''
import pickle
import pymongo
import os.path
from src import Config
from src import Utils

if __name__ == '__main__':
    user_id = 'b42c916c-3b1e-4235-85b7-451aea401218' #modify later for specific user
    conn = pymongo.MongoClient(Config.config['mongo_url'])
    db = conn.VoiceImageDB
    coll = db.voice_images
    docs = coll.find()
    
    indexer = [[], []]
    
    for doc in docs:
        indexer[0].append(doc['time'])
        indexer[1].append(doc['image_name'])
        
    filename = Utils.get_user_path(user_id) + "/" + "time_indexer.dat"
    if not os.path.isfile(filename):
        os.remove(filename)
     
    with open(filename,'wb') as fp:
        pickle.dump(indexer,fp)
    fp.close()
         
    with open(filename,'rb') as fp:
            indexer_read = pickle.load(fp)
    fp.close()
    
    print(indexer_read[0])
    print(len(indexer_read[1]))