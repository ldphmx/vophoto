#Encoding=UTF8

import tornado.web
import MongoHelper
import json
import Utils
import BaseAuthenticateHandler
import NLPTimeConvertor

class SearchHandler(BaseAuthenticateHandler.BaseAuthenticateHandler):
    def post(self):
        result = {'status': False}
        try:
            user_id = self.get_argument('user_id', '')
            desc = self.get_argument('desc','')   #add
            rawTag = self.get_argument('tag', '')
            # 我_r 想_v 找_v 去年_nt 夏天_nt 在_p 西雅图_ns 农贸市场_n 的_u 照片_n
        ###peigang
            rawLocation = self.get_argument('loc','')
            token = self.get_argument('token','')
            user = MongoHelper.get_user_by_id(user_id)
            if token != user['token']:
                self.write(json.dumps(result))
                return
        
            if user_id == '' or rawTag == '':
                self.write(json.dumps(result))
                return
       
            key_location = rawLocation.split(',')
            latitude = float(key_location[0])
            longitude = float(key_location[1])  
            image_to_client = []
            key_words = rawTag.split(' ')
            if key_words is None or len(key_words) == 0:
                self.write(json.dumps(result))
                return
            meaningful = Utils.get_meaningful_keywords(key_words)
            face_id = Utils.get_faceid_from_rawTags(rawTag)
            if face_id is not None:
                meaningful.append(face_id)
            
            raw_image  = Utils.get_images_by_tag(user_id, meaningful)   ##需修改这个函数：search时容错、关联度
            
            #get time_range#
            time_range = NLPTimeConvertor.time_api(rawTag)

            
            if key_location is None and time_range is None:    
                image = raw_image
            elif key_location is None and time_range is not None:   
                image = Utils.get_image_depend_timerange(raw_image,time_range)
            elif key_location is not None and time_range is not None:
                Traw_image = Utils.get_image_depend_timerange(raw_image,time_range)
                image = Utils.get_images_by_location_from_photos(latitude, longitude,Traw_image)
            else:
                image = Utils.get_images_by_location_from_photos(latitude, longitude,raw_image)   
            for item in image:
                image_info = item[0]
                image_to_client.append(image_info['img_name'])
            
            result['status'] = True
            result['image'] = image_to_client
            
        finally:
            self.write(json.dumps(result))
