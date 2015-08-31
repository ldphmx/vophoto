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
        index_images = []
        for image in images:
            x = image['location']['longtude']
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
    
    pts = np.array(indexer[0])
    tree = spatial.KDTree(pts)
    loc_point = np.array([location[0], location[1]])
    results = tree.query(loc_point, k=len(indexer[1]))  #[[distance],[index]]
    for res_index in results[1]:
        sorted_images.append(indexer[1][res_index])
    return sorted_images

if __name__ == '__main__':
    pass