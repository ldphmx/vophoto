#Encoding=UTF8

import Config
import time
import MongoHelper
import Utils
import FaceUtils
import uuid

def process_images(num):
    images = MongoHelper.get_unprocessed(num)
    for image in images:
        process_location(image)
        process_desc(image)
        process_faces(image)
        MongoHelper.save_image(image)
    
def process_location(image):
    tags = image.get('tags', [])
    image['tags'] = tags

def process_desc(image):
    tags = image.get('tags', [])
    raw = image.get('desc', '')
    if not raw:
        return
    
    key_words = raw.split(' ')
    if key_words is None or len(key_words) == 0:
        return
    
    meaningful = Utils.get_meaningful_keywords(key_words)
    for t in meaningful:
        if not t in tags:
            tags.append(t)
            
    image['tags'] = tags

def process_faces(image):
    tags = image.get('tags', [])
    user_id = image.get('user_id', '')
    if not user_id:
        return
    
    exists = FaceUtils.is_person_group_exists(user_id)
    if not exists:
        FaceUtils.create_person_group(user_id)
        
    image_name = image.get('image_name', '')
    if not image_name:
        return
    
    names = Utils.get_human_names(image.get('desc', ''))
    names.reverse()
    faces = FaceUtils.detect_faces_in_photo(Utils.get_user_path(user_id) + "/" + image_name)
    result = FaceUtils.identify_faces(user_id, faces)
    
    for res in result:
        face_id = res['faceId']
        target_id = ''
        candidates = res.get('candidates', [])
        if len(candidates) > 0:
            target_id = candidates[0]
        
        if target_id:
            tags.append(target_id)
        else:
            person_id = FaceUtils.create_person(user_id, [face_id], uuid.uuid4())
            FaceUtils.train_person_group_wait(user_id)
            person = {'person_id': person_id, 'name': names.pop()}
            MongoHelper.save_person(person)
    
    image['tags'] = tags
    
if __name__ == "__main__":
    while True:
        process_images(Config.config['image_process_batch'])
        time.sleep(1)
        

