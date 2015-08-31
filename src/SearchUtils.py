'''
Created on Aug 28, 2015

@author: v-shayi
'''
from src import Config
import os
from pymemcache.client.base import Client
from scipy import spatial
import numpy as np
from hashlib import md5
import pickle

mc = Client((Config.config['memcached_host'], 11211))

def get_user_path(userId):
    md5ins = md5()
    md5ins.update(userId)
    md5str = md5ins.hexdigest()
    path = Config.config['photo_root'] + md5str[0:2] + "/" + md5str[2:4] + "/" + md5str[4:6] + "/" + userId
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def sort_by_location(latitude, longitude, image_list):
    sorted_images = []
    if not image_list:
        return None
    
    for images in image_list:
        index_images = [[],[]]
        for image in images:
            x = image['location']['longitude']
            y = image['location']['latitude']
            index_images[0].append([x, y])
            index_images[1].append(image['image_name'])
# index_images = [[[14.32, 15.32], [0.89, 0.56], [6.36, 3.66]], ['img01', 'img03', 'img04']]
        res_image_list = sort_by_closest_point(index_images, longitude, latitude)
        sorted_images += res_image_list
    return sorted_images


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
    filename = 'time_indexer.dat'    # modify later when md5str available
    if not os.path.exists(filename):
        time_indexer = {}
    else:
        with open(filename,'rb') as fp:
            time_indexer = pickle.load(fp)
    time_sorted_imgs = sort_image_by_time(time_indexer, time_list)
    return time_sorted_imgs

def sort_image_by_time(img_list, time_ranges):
    # time_list: [(st, et), (st, et)]
    # img_list: [[t1, t2], [img1, img2]]
    sort_img = []
    for time_range in time_ranges:
        for time in img_list[0]:
            if time > time_range[1]:
                break
            elif time > time_range[0]:
                sort_img.append(img_list[1][img_list[0].index(time)])
    return sort_img

if __name__ == '__main__':
    imageList = [[{'image_name': 'img02.jpg', 'location': {'longitude': 45.123456, 'latitude': 25.456789}},
                  {'image_name': 'img01.jpg', 'location': {'longitude': 14.123456, 'latitude': 15.456789}},
                 {'image_name': 'img03.jpg', 'location': {'longitude': 40.123456, 'latitude': 85.456789}}],
                 [{'image_name': 'img04.jpg', 'location': {'longitude': 45.123456, 'latitude': 25.456789}},
                  {'image_name': 'img05.jpg', 'location': {'longitude': 15.123456, 'latitude': 16.456789}}]]
    sorted_imgs = sort_by_location(14.123001, 15.456001, imageList)
    print(sorted_imgs)