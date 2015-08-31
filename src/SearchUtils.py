'''
Created on Aug 28, 2015

@author: v-shayi
'''
from src import Config
import os
from pymemcache.client.base import Client
from scipy import spatial
import numpy as np

def sort_by_location(image_list, location):
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
        res_image_list = sort_by_closest_point(index_images, location)
        sorted_images += res_image_list
    return sorted_images


def sort_by_closest_point(indexer, location):
    sorted_images = []
    if not indexer:
        return None
    if len(indexer[1]) is 1:
        return indexer[1]
    
    pts = np.array(indexer[0])
    tree = spatial.KDTree(pts)
    loc_point = np.array([location['longitude'], location['latitude']])
    results = tree.query(loc_point, k=len(indexer[1]))  #[[distance],[index]]
    test = results[1]
    for res_index in results[1]:
        sorted_images.append(indexer[1][res_index])
    return sorted_images

if __name__ == '__main__':
    imageList = [[{'image_name': 'img02.jpg', 'location': {'longitude': 45.123456, 'latitude': 25.456789}},
                  {'image_name': 'img01.jpg', 'location': {'longitude': 14.123456, 'latitude': 15.456789}},
                 {'image_name': 'img03.jpg', 'location': {'longitude': 40.123456, 'latitude': 85.456789}}],
                 [{'image_name': 'img04.jpg', 'location': {'longitude': 45.123456, 'latitude': 25.456789}},
                  {'image_name': 'img05.jpg', 'location': {'longitude': 15.123456, 'latitude': 16.456789}}]]
    sorted_imgs = sort_by_location(imageList, {'longitude': 14.123001, 'latitude': 15.456001})
    print(sorted_imgs)