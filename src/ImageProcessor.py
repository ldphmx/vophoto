#Encoding=UTF8

import Config
import time
import MongoHelper

def process_images(num):
    images = MongoHelper.get_unprocessed(num)
    for image in images:
        process_location(image)
        process_desc(image)
        process_faces(image)
    
def process_location(image):
    pass

def process_desc(image):
    pass

def process_faces(image):
    pass

if __name__ == "__main__":
    while True:
        process_images(Config.config['image_process_batch'])
        time.sleep(1)
        

