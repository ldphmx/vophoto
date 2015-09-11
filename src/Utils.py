#Encoding=UTF8

import Config
from hashlib import md5
import os
import MongoHelper
import pickle
import pypinyin
import bmemcached
from scipy import spatial
import numpy as np
import json
import aiohttp
import http.client
from fuzzywuzzy import fuzz
from datetime import datetime
import Logger
from itertools import combinations
import time
import bisect

mc = bmemcached.Client((Config.config['memcached_host'],))

def get_similar_tags(user_id, input_tags):
    filename = get_user_path(user_id) + "/" + "image_indexer.dat"
    stored_tags = mc.get(user_id + "_image")
    if not stored_tags:
        if not os.path.exists(filename):
            stored_tags = [[],[]]
        else:
            with open(filename,'rb') as fp:
                stored_tags = pickle.load(fp)
          
    if stored_tags is None:
        return None
    
    Logger.debug('indexer keys: ' + str(stored_tags[0]))
    result = []
    for input_tag in input_tags:
        rate_index = []
        tag_list = []
        for stored_tag in stored_tags[0]:
            rate = fuzz.ratio(input_tag, stored_tag)
            if rate >= 80:
                tag_list.insert(bisect.bisect(rate_index, rate), stored_tag)
                bisect.insort(rate_index, rate)
        result.append(tag_list)
    
    return result
             

def update_image_indexer(user_id, img):
    filename = get_user_path(user_id) + "/" + "image_indexer.dat"
    indexer = mc.get(user_id + "_image")
    if not indexer:
        if not os.path.exists(filename):
            indexer = {}
        else:
            with open(filename,'rb') as fp:
                indexer = pickle.load(fp)
    
    if indexer is None:
        return
    
    for tag in img['tags']:
        if indexer[0].count(tag) is 0:
            indexer[0].append(tag)
            indexer[1].append([img['image_name']])
        else:
            tag_index = indexer[0].index(tag)
            indexer[1][tag_index].append(img['image_name'])
    
    with open(filename,'wb') as fp:
        pickle.dump(indexer,fp)
    
    mc.set(user_id + "_image", indexer)
    Logger.debug('image indexer updated: ' + str(indexer))

def get_user_path(userId):
    md5ins = md5()
    md5ins.update(userId.encode())
    md5str = md5ins.hexdigest()
    path = Config.config['photo_root'] + md5str[0:2] + "/" + md5str[2:4] + "/" + md5str[4:6] + "/" + userId
    if not os.path.exists(path):
        os.makedirs(path)
    Logger.debug('user path:' + path)
    return path
    
def generate_access_token(userId):
    md5ins = md5()
    md5ins.update(userId.encode())
    md5ins.update(Config.config['access_token'].encode())
    return md5ins.hexdigest()

def get_images_by_tags_array(user_id, tags_list, image):
    Logger.debug('get_images_by_tags_array: ' + str(tags_list))
    image_res = []
    for tags in tags_list:
        img_list = get_image_by_tags(user_id, tags)
        image_res.append(set(img_list))
    image_res.append(set(image))
    
    Logger.debug('get_images_by_tags_array set list: ' + str(image_res))
    #[[set(), set()...]]
    inter_sec = []
    if len(image_res) > 1:
        for i in range(1, len(image_res) + 1):
            inter = []
            for i in combinations(image_res, i):
                res = set.intersection(*i)
                inter.append(res)
                
            inter_sec.append(inter)
    else:
        inter_sec = [image_res]
    
    final_list = []
    inter_sec.reverse()
    image_pool = set()
    for i in inter_sec:
        for s in i:
            if not s in final_list:
                insert_set = s - (s & image_pool)
                if insert_set:
                    final_list.append(insert_set)
                image_pool  = image_pool | s
            
    return final_list
    

def get_image_by_tags(user_id, tags):
    list = []
    indexer = get_image_indexer(user_id)
    for tag in tags:
        if indexer[0].count(tag) > 0:
            items = indexer[1][indexer[0].index(tag)]
            for item in items:
                if not item in list:
                    list.append(item)
            
    return list

def get_image_indexer(user_id):
    filename = get_user_path(user_id) + "/" + "image_indexer.dat"
    tag_img = mc.get(user_id + "_image")
    if not tag_img:
        if not os.path.exists(filename):
            tag_img = [[],[]]
        else:
            with open(filename,'rb') as fp:
                tag_img = pickle.load(fp)
        mc.set(user_id + "_image", tag_img)  
          
    if tag_img is None:
        return None

    return tag_img

    
def get_meaningful_keywords(key_words):
    keys = []
    for k in key_words:
        pair = k.split('_')
        if pair is None or len(pair) < 2:
            continue
        
        if pair[1] in Config.config['meaningful_pos']:
            keys.append(pypinyin.slug(pair[0]))
    return keys

def get_object_keywords(key_words):
    keys = []
    for k in key_words:
        pair = k.split('_')
        if pair is None or len(pair) < 2:
            continue
        
        if pair[1] in Config.config['object_pos']:
            keys.append(pypinyin.slug(pair[0]))
    return keys

def get_location_from_rawlocation(key_location):
    location = {}
    location['longitude'] = float(key_location[0])
    location['latitude'] = float(key_location[1])
    return location

def get_user_photo_indexer(user_id):
    indexer = mc.get(user_id)
    if indexer is not None:
        return indexer
    
    filename = get_user_path(user_id) + "/" + "indexer.dat"
    if not os.path.exists(filename):
        indexer = {}
    else:
        with open(filename,'rb') as fp:
            indexer = pickle.load(fp)
        
    mc.set(user_id + "_location", indexer)
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

def translate_tags(tags):
    Logger.debug('translate_tags in')
    cv_tags = mc.get('cv_tags')
    if not cv_tags:
        Logger.debug('translate_tags load from file')
        cv_tags = load_cv_tags()
        mc.set('cv_tags', cv_tags)
    
    Logger.debug('translate_tags 3')
    ret = []
    pytags = [pypinyin.slug(w) for w in tags]
    for tag in pytags:
        cand = cv_tags.get(tag, [])
        ret.extend(cand)
        
    return ret

def create_face_group(user_id):
#     host = 'https://api.projectoxford.ai/asia/face/v0'
    res = False
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': Config.config['face_api_key'],
    }
    
    body = {'name': user_id.lower()}
    
    try:
        conn = http.client.HTTPSConnection("api.projectoxford.ai")
        conn.request("PUT", "/asia/face/v0/facegroups/%s" % user_id.lower(), body=json.dumps(body), headers=headers)
        response = conn.getresponse()
        data = response.read()
        res = response.status == 200
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    finally:
        return res
    
def load_cv_tags():
    cv_tags = {}
    path = os.path.dirname(os.path.realpath(__file__)) + "/category.txt"
    if not os.path.exists(path):
        return {}
    
    file = open(path, encoding="utf-8")
    for line in file:
        items = line.strip().split(':')
        tag = items[0]
        words = [pypinyin.slug(w) for w in items[1].split('-')]
        for word in words:
            if not word in cv_tags.keys():
                cv_tags[word] = []
            cv_tags[word].append(tag)
    
    return cv_tags

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
            keys.append(pypinyin.slug(pair[0]))
        
    return keys
    
def get_images_by_tag(user_id, input_tags, image):
    if not image:
        return []
    
    if not input_tags:
        return image
    
    Logger.debug('get_images_by_tag: ' + str(input_tags))
    tags_list = get_similar_tags(user_id, input_tags)
    Logger.debug('get_images_by_tag similar: ' + str(tags_list))
    if not tags_list:
        return []
    else:
        result = get_images_by_tags_array(user_id, tags_list, image)
        if result:
            return result
        else:
            return [set(image)]
        
    Logger.error('Error in get_images_by_tag')
    return None

def sort_by_location(user_id, latitude, longitude, image_list):  
    if not image_list:
        return []
    
    result = []
    if latitude is None or longitude is None:
        for image in image_list:
            result.extend(image)
        return result
    
    filename = get_user_path(user_id) + "/" + "location_indexer.dat"
    loc_indexer = mc.get(user_id + "_location")
    if not loc_indexer:
        if not os.path.exists(filename):
            loc_indexer = [[], []]
            for image in image_list:
                result.extend(image)
            return result
        else:
            with open(filename,'rb') as fp:
                loc_indexer = pickle.load(fp)
        mc.set(user_id + "_location", loc_indexer)
    
    # index_images = [[[14.32, 15.32], [0.89, 0.56], [6.36, 3.66]], ['img01', 'img03', 'img04']]
    for image_set in image_list:
        unsorted_images = [[], []]
        for image in image_set:
            unsorted_images[0].append(loc_indexer[0][loc_indexer[1].index(image)])
            unsorted_images[1].append(image)
        sorted_image = sort_by_closest_point(unsorted_images, longitude, latitude)
        result.extend(sorted_image)
        
    if result:
        return result
    else:
        Logger.error("Error in sort_by_location")
        return None

def sort_by_closest_point(indexer, longitude, latitude):
    sorted_images = []
    if not indexer:
        return None
    if len(indexer[1]) is 1:
        return indexer[1]
    
    pts = np.array(indexer[0])
    tree = spatial.KDTree(pts)
    loc_point = np.array([longitude, latitude])
    results = tree.query(loc_point, k=len(indexer[1]))  #[[distance],[index]]
    for res_index in results[1]:
        sorted_images.append(indexer[1][res_index])
    return sorted_images

def get_image_by_time(user_id, time_list):
    filename = get_user_path(user_id) + "/" + "time_indexer.dat"
    time_indexer = mc.get(user_id + "_time")
    if not time_indexer:
        if not os.path.exists(filename):
            time_indexer = []
        else:
            with open(filename,'rb') as fp:
                time_indexer = pickle.load(fp)
        mc.set(user_id + "_time", time_indexer)
         
    if not time_indexer:
        return []

    return sort_image_by_time(time_indexer, time_list)

def sort_image_by_time(img_list, time_ranges):
    # time_list: [(st, et), (st, et)]
    # img_list: [[t1, t2], [img1, img2]]
    Logger.debug('img_list:' + str(img_list))
    Logger.debug('time_ranges' + str(time_ranges))
    sort_img = []
    
    if not time_ranges:
        return img_list[1]
    
    for time_range in time_ranges:
        for time in img_list[0]:
            if time > time_range[1]:
                break
            elif time >= time_range[0]:
                sort_img.append(img_list[1][img_list[0].index(time)])
    Logger.debug('sorted img list: ')
    Logger.debug(sort_img)
    
    if not sort_img:
        return img_list[1]
    return sort_img
    
def update_time_indexer(user_id, input_img_time):
    indexer = [[], []]
    filename = get_user_path(user_id) + "/" + "time_indexer.dat"
     
    if os.path.isfile(filename):
        with open(filename,'rb') as fp:
            indexer = pickle.load(fp)
    else:
        indexer = [[input_img_time['time']], [input_img_time['image_name']]]
            
    # img_list: [[t1, t2], [img1, img2]]
    indexer[1].insert(bisect.bisect(indexer[0], input_img_time['time']), input_img_time['image_name'])
    bisect.insort(indexer[0], input_img_time['time'])
    
    with open(filename, 'wb') as fp:
        pickle.dump(indexer,fp)
        
    mc.set(user_id + "_time", indexer)
    Logger.debug('time indexer updated:' + str(indexer))

if __name__ == "__main__":
    print(get_images_by_tag('127f46fc-f21e-4911-a734-be4abfa8b318', ['test', 'xia-tian', 'bin-ma-yong'], ["IMG_1330.JPG", "IMG_1331.JPG","IMG_1332.JPG", "IMG_1347.JPG", "IMG_1367.JPG"]))
#     print(pypinyin.slug((u'测试test')))
#     image = {'tags': ['a','b'], 'image_name':'y.jpg'}
#     update_user_photo_indexer('xxx', image)
#     print get_user_photo_indexer('xxx')
