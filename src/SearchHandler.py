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
            face_name = Utils.get_human_names(rawTag)
            face_id = list(MongoHelper.get_similar_persons(user_id,face_name))  
            if face_id is not None:
                meaningful.append(face_id)
            
            time_range = NLPTimeConvertor.time_api(rawTag)
            if time_range is not None and key_location is not None:
                Timage = Utils.get_image_by_time(user_id, time_range)    ##yisa
                Tag_image = Utils.get_images_by_tag_from_Timage(user_id,meaningful,Timage)
                image = Utils.sort_by_location(latitude,longitude,Tag_image)
            elif time_range is not None and key_location is None:
                Timage = Utils.get_image_depend_timerange_from_index(time_range)
                image = Utils.get_images_by_tag_from_Timage(user_id,meaningful,Timage)
            elif time_range is None and key_location is not None:
                Tag_image = Utils.get_images_by_tag(user_id, meaningful)
                image = Utils.sort_by_location(latitude,longitude,Tag_image)
            elif time_range is None and key_location is None:
                image = Utils.get_images_by_tag(user_id, meaningful)
                
            for item in image:
                image_to_client.append(item)
                
            result['status'] = True
            result['image'] = image_to_client


        finally:
            self.write(json.dumps(result))
