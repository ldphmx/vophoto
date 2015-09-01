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
            
            key_words = rawTag.split(' ')
            if key_words is None or len(key_words) == 0:
                self.write(json.dumps(result))
                return
            meaningful = Utils.get_meaningful_keywords(key_words)
            face_name = Utils.get_human_names(rawTag)
            face_id = list(MongoHelper.get_similar_persons(user_id,face_name))  
            if face_id :
                meaningful.extend(face_id)
            object_name = Utils.get_object_keywords(key_words)
            cv_tags = Utils.translate_tags(object_name)
            if cv_tags:
                meaningful.extend(cv_tags)
            
            time_range = NLPTimeConvertor.time_api(rawTag)
            if time_range and key_location:
                Timage = Utils.get_image_by_time(user_id, time_range)    
                Tag_image = Utils.get_images_by_tag_from_Timage(user_id,meaningful,Timage,1)
                image = Utils.sort_by_location(latitude,longitude,Tag_image)
            elif time_range and not key_location:
                Timage = Utils.get_image_by_time(user_id, time_range)
                image = Utils.get_images_by_tag_from_Timage(user_id,meaningful,Timage,0)
            elif not time_range and key_location:
                Tag_image = Utils.get_images_by_tag(user_id, meaningful,1)
                image = Utils.sort_by_location(latitude,longitude,Tag_image)
            elif not time_range and not key_location:
                image = Utils.get_images_by_tag(user_id, meaningful,0)
                
            
                
            result['status'] = True
            result['image'] = image


        finally:
            self.write(json.dumps(result))
