#Encoding=UTF8

import Config
from hashlib import md5
import os
import MongoHelper
import pickle
import pypinyin
from pymemcache.client.base import Client

mc = Client((Config.config['memcached_host'], 11211))

def get_user_path(userId):
    md5ins = md5.new()
    md5ins.update(userId)
    md5str = md5ins.hexdigest()
    path = Config.config['photo_root'] + md5str[0:2] + "/" + md5str[2:4] + "/" + md5str[4:6] + "/" + userId
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def allocate_user_server(userId):
    servers = Config.config['servers']
    if len(servers) == 0:
        return None
    
    server_usage = MongoHelper.get_server_users()
    for name in server_usage:
        count = server_usage[name]
        capacity = 0
        for server in servers:
            if server['name'] == name:
                capacity = server['capacity']
                break
        
        if count >= capacity:
            continue
        else:
            return name
    
    return None
    
    
def generate_access_token(userId):
    md5ins = md5.new()
    md5ins.update(userId)
    md5ins.update(Config.config['access_token'])
    return md5ins.hexdigest()

def get_meaningful_keywords(key_words):
    keys = []
    for k in key_words:
        pair = k.split('_')
        if pair is None or len(pair) < 2:
            continue
        
        if pair[1] in Config.config['meaningful_pos']:
            keys.append(pair[0])
        
    
    return keys

def get_user_photo_indexer(user_id):
    indexer = mc.get(user_id)
    if indexer is not None:
        return indexer
    
    filename = get_user_path(user_id) + "/" + "indexer.dat"
    with open(filename,'rb') as fp:
        indexer = pickle.load(fp)
        
    mc.set(user_id, indexer)
    return indexer
    
def update_user_photo_indexer(user_id, image):
    filename = get_user_path(user_id) + "/" + "indexer.dat"
    indexer = mc.get(user_id)
    if not indexer:
        if not os.path.exists(filename):
            indexer = {}
        else:
            with open(filename,'rb') as fp:
                indexer = pickle.load(fp)
    
    if indexer is None:
        return
    
    tags = image['tags']
    image_name = image['image_name']
    
    for t in tags:
        pt = pypinyin.slug(t)
        photo_list = indexer.get(pt, [])
        photo_list.append(image_name)
        indexer[pt] = photo_list
    
    with open(filename,'wb') as fp:
        pickle.dump(indexer,fp)
    
    mc.set(user_id, indexer)
    return indexer

def search_images_by_tags(user_id, tags):
    images = []
    indexer = get_user_photo_indexer(user_id)
    if not indexer:
        return images
    
    for tag in tags:
        photo_list = indexer[tag]
        images.append(photo_list)
        
    return images

def get_human_names(raw):
    keys = []
    key_words = raw.split(' ')
    if key_words is None or len(key_words) == 0:
        return
    
    for k in key_words:
        pair = k.split('_')
        if pair is None or len(pair) < 2:
            continue
        
        if pair[1] in Config.config['human_name_pos']:
            keys.append(pair[0])
        
    return keys

###########added by yisha####################
# search in db for nearby img
# input float latitude longitude 
def get_images_by_location(user_id, latitude, longitude, distance=0.01):
    image_sort = []
    image_unsort = []
    user_img = MongoHelper.get_images_by_user(user_id)
    for img in user_img:
        abs_lat = abs(img['lat'] - latitude)
        abs_lon = abs(img['lon'] - longitude)
        if abs_lat < distance & abs_lon < distance:
            temp = ((abs_lat + abs_lon), img)
            image_unsort.append(temp)
    image_sort = sorted(image_unsort, key=lambda img: img[0])
    return image_sort

if __name__ == "__main__":
    print(pypinyin.slug((u'测试test')))
#     image = {'tags': ['a','b'], 'image_name':'y.jpg'}
#     update_user_photo_indexer('xxx', image)
#     print get_user_photo_indexer('xxx')
    
    
    
