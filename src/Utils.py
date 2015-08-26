#Encoding=UTF8

import Config
from hashlib import md5
import os
import MongoHelper
import pickle
import pypinyin
from pymemcache.client.base import Client
from scipy import spatial
import numpy as np

mc = Client((Config.config['memcached_host'], 11211))

def get_user_path(userId):
    md5ins = md5()
    md5ins.update(userId)
    md5str = md5ins.hexdigest()
    path = Config.config['photo_root'] + md5str[0:2] + "/" + md5str[2:4] + "/" + md5str[4:6] + "/" + userId
    if not os.path.exists(path):
        os.makedirs(path)
    return path
    
def generate_access_token(userId):
    md5ins = md5()
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

##added by peigang
def get_location_from_rawlocation(key_location):
    location = {}
    location['longitude'] = float(key_location[0])
    location['latitude'] = float(key_location[1])
    return location
        
def get_tag_from_rawlocation(key_location):
    tags = key_location[2:]
    return tags
##added by peigang

def get_user_photo_location_indexer(user_id):
    indexer = mc.get(user_id + '_location')
    if indexer is not None:
        return indexer
    
    filename = get_user_path(user_id) + "/" + "loc_indexer.dat"
    with open(filename,'rb') as fp:
        indexer = pickle.load(fp)
        
    mc.set(user_id, indexer)
    return indexer

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

def get_closest_points(user_id, point):
    indexer = get_user_photo_location_indexer(user_id)
    if not indexer:
        return None
    
    pts = np.array(indexer[0])
    tree = spatial.KDTree(pts)
    res = tree.query(point, k=len(indexer[1]))
    
    print(res)

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
'''
Search in db for nearby img by location
@return: sorted image dictionary by distance  
'''
def get_images_by_location(user_id, latitude, longitude, distance=1):
    image_unsort = []
    user_img = MongoHelper.get_images_by_user(user_id)
    location = user_img['location']           #update by peigang
    for img in user_img:
        abs_lat = abs(location['latitude'] - latitude)     #update by peigang
        abs_lon = abs(location['longitude'] - longitude)   #update by peigang
        if abs_lat < distance & abs_lon < distance:
            temp = ((abs_lat + abs_lon), img)
            image_unsort.append(temp)
    image_sort = sorted(image_unsort, key=lambda img: img[0])
    return image_sort[1]            #update by peigang

'''
Search in db for img with input tags
@return: sorted image dictionary by tags, ordered by time
'''
##added by peigang
def get_images_by_location_from_photos(latitude, longitude,certain_photo):
    image_unsort = []
    user_img = certain_photo
    for img in user_img:
        abs_lat = abs(img['lat'] - latitude)
        abs_lon = abs(img['lon'] - longitude)
        if abs_lat < 1 & abs_lon < 1:
            temp = ((abs_lat + abs_lon), img)
            image_unsort.append(temp)
    image_sort = sorted(image_unsort, key=lambda img: img[0])
    return image_sort[1]                               
##added by peigang

def get_images_by_tag(user_id, input_tags):
    image_unsort = []
    tags = set(input_tags)
    user_img = MongoHelper.get_images_by_user(user_id)
    for img in user_img:
        user_tags = set(user_img['tags'])
        if tags.issubset(user_tags):
            image_unsort.append(img)
    image_sort = sorted(image_unsort, key=lambda img: img[6], reversed=True)   #time object at 6 index in image dictionary
    return image_sort

##added by peigang##
def get_image_depend_timerange(raw_image,time_range):
    image_unsort = []
    user_img = raw_image
    for img in user_img:
        for item in time_range:
            if img['time'] < item[1] and img['time'] > item[0]:
                image_unsort.append(img)
    return image_unsort 

if __name__ == "__main__":
    get_closest_points('wang', [0,0])
#     print(pypinyin.slug((u'测试test')))
#     image = {'tags': ['a','b'], 'image_name':'y.jpg'}
#     update_user_photo_indexer('xxx', image)
#     print get_user_photo_indexer('xxx')
    
    
    
