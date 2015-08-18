#Encoding=UTF8

import httplib, urllib, base64
import Config
import json
import time
import os
import uuid
    
def is_person_group_exists(user_id):
    res = False
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': Config.config['face_api_key'],
    }
    
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("GET", "/face/v0/persongroups/%s" % user_id, None, headers)
        response = conn.getresponse()
        data = response.read()
        if response.status == 200:
            res = True
        conn.close()
    finally:
        return res
        
    return res
    
def create_person_group(user_id):
    res = False
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': Config.config['face_api_key'],
    }
    
    body = {'name': user_id}
    
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("PUT", "/face/v0/persongroups/%s" % user_id, json.dumps(body), headers)
        response = conn.getresponse()
        if response.status == 200:
            res = True
        conn.close()
    finally:
        return res

def delete_person_group(user_id):
    res = False
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': Config.config['face_api_key'],
    }
    
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("DELETE", "/face/v0/persongroups/%s" % user_id, "{body}", headers)
        response = conn.getresponse()
        if response.status == 200:
            res = True
        conn.close()
    finally:
        return res

def detect_faces_in_photo(image):
    faces = []
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': Config.config['face_api_key'],
    }
    
    params = urllib.urlencode({
        # Request parameters
        'analyzesFaceLandmarks': 'false',
        'analyzesAge': 'false',
        'analyzesGender': 'false',
        'analyzesHeadPose': 'false',
    })
    
    try:
        image_bin = open(image, 'rb')
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v0/detections?%s" % params, image_bin, headers)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            face_json = json.loads(data)
            for face in face_json:
                faces.append(face['faceId'])
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    finally:
        return faces
    
def identify_faces(user_id, faces):
    faces_res = []
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': Config.config['face_api_key'],
    }
    
    body = {'faceIds': faces, 'personGroupId': user_id, 'maxNumOfCandidatesReturned':1}
    
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v0/identifications", json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read()
        json_data = json.loads(data)
        conn.close()
        if response.status == 200:
            faces_res = json_data
            return faces_res
            
        if response.status == 400:
            result = json_data['code']
            return result
            
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return None

def create_person(user_id, faces, name):
    person_id = ''
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': Config.config['face_api_key'],
    }
    
    body = {'faceIds': faces, 'name': user_id, 'userData':""}
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v0/persongroups/%s/persons" % user_id, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        
        if response.status == 200:
            json_str = json.loads(data)
            person_id = json_str.get('personId', '')
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    finally:
        return person_id
    
def train_person_group(user_id):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': Config.config['face_api_key'],
    }

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v0/persongroups/%s/training" % user_id, '', headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
def train_person_group_wait(user_id):
    train_person_group(user_id)
    status = get_training_status(user_id)
    while status == 'running':
        time.sleep(1)
        status = get_training_status(user_id)
      
def get_training_status(user_id):
    status = ''
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': Config.config['face_api_key'],
    }
    
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("GET", "/face/v0/persongroups/%s/training" % user_id, None, headers)
        response = conn.getresponse()
        if response.status == 200:
            data = response.read()
            stat_json = json.loads(data)
            status = stat_json['status']
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    finally:
        return status
    
def train_default(user_id):
    create_person_group(user_id)
    faces = detect_faces_in_photo(os.path.dirname(os.path.realpath(__file__)) + "/demo.jpg")
    person_id = create_person(user_id, faces, uuid.uuid4())
    train_person_group_wait(user_id)
    delete_person(user_id, person_id)
    
def delete_person(user_id, person_id):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': Config.config['face_api_key'],
    }
    
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("DELETE", "/face/v0/persongroups/%s/persons/%s" % (user_id, person_id), "", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
if __name__ == "__main__":
    group = 'xxx'
    delete_person_group(group)
    
    start = time.time()
    train_default(group)
    end = time.time()
    
    print end - start
#     create_person_group(group)
#     
#     faces = detect_faces_in_photo('E:/data/2.jpg')
#     create_person(group, faces, 'wang')
#     train_person_group(group)
#     
#     status = get_training_status(group)
#     while status == 'running':
#         time.sleep(1)
#         status = get_training_status(group)
    
#     faces = detect_faces_in_photo('E:/data/2.jpg')
#     print identify_faces(group, faces)
    
    