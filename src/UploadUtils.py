'''
Created on Aug 28, 2015

@author: v-shayi
'''
from src import Config
from hashlib import md5
import os
from src import MongoHelper
import pickle
import pypinyin
from pymemcache.client.base import Client
from scipy import spatial
import numpy as np
from datetime import datetime

mc = Client((Config.config['memcached_host'], 11211))

def get_user_path(userId):
    md5ins = md5()
    md5ins.update(userId)
    md5str = md5ins.hexdigest()
    path = Config.config['photo_root'] + md5str[0:2] + "/" + md5str[2:4] + "/" + md5str[4:6] + "/" + userId
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def update_time_indexer(user_id, input_img_time):
    indexer = mc.get(user_id + '_time')
#     filename = get_user_path(user_id) + "/" + "time_indexer.dat"
    filename = 'time_indexer.dat'
     
    if not indexer:
        indexer = [[input_img_time['time']], [input_img_time['image_name']]]
        mc.set(user_id, indexer)
    else:    
        with open(filename,'rb') as fp:
            indexer = pickle.load(fp)
    
    # img_list: [[t1, t2], [img1, img2]]
    imgs = []
    new_indexer = [[], []]
    i = 0
    while i < len(indexer[0]):
        img = {'time': indexer[0][i], 'image_name': indexer[1][i]}
        imgs.append(img)
        i += 1
    img = {'time': input_img_time['time'], 'image_name': input_img_time['image_name']}
    imgs.append(img)
    image_sort = sorted(imgs, key=lambda img: img['time'])
    for img in image_sort:
        new_indexer[0].append(img['time'])
        new_indexer[1].append(img['image_name'])
    mc.set(user_id, new_indexer)
    
    with open(filename, 'wb') as fp:
        pickle.dump(new_indexer,fp)
        
    print(new_indexer)
    
if __name__ == '__main__':
    initTime = '1996-01-03 00:00:00 +0800'
    myInitTime1 = datetime.strptime(initTime, '%Y-%m-%d %X %z')
    update_time_indexer('001', {'image_name': 'img11.jpg', 'time': myInitTime1, 'location': [10.2, 50.223]})