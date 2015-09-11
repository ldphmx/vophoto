#Encoding=UTF8

import tornado.web
import Logger
import MongoHelper
import json
import Utils
import BaseAuthenticateHandler
import NLPTimeConvertor

class SearchHandler(BaseAuthenticateHandler.BaseAuthenticateHandler):
    def post(self):
        result = {'status': False}
        Logger.debug('in search')
        try:
            user_id = self.get_argument('user_id', '')
            desc = self.get_argument('desc','')
#             desc = ['我_r 想_v 找_v 在_p 天安门_ns 的_u 照片_n']
            rawTag = self.get_argument('tag', '')
#             rawTag = '我_r 想_v 找_v 去年_nt 夏天_nt 的_u 照片_n'
            # 我_r 想_v 找_v 去年_nt 夏天_nt 在_p 西雅图_ns 农贸市场_n 的_u 照片_n
            rawLocation = self.get_argument('loc','')
            token = self.get_argument('token','')
            user = MongoHelper.get_user_by_id(user_id)
            Logger.info('user_id:' + user_id + ', raw tag:' + ', raw location:' + ', token:' + token)
            
            if token is not user['token']:
                self.write(json.dumps(result))
                Logger.debug('token wrong')
                return
        
            if user_id == '' or rawTag == '':
                Logger.debug('user id or tag null')
                self.write(json.dumps(result))
                return

            key_words = rawTag.split(' ')
            if key_words is None or len(key_words) == 0:
                Logger.debug('key words none')
                self.write(json.dumps(result))
                return
            
            meaningful = Utils.get_meaningful_keywords(key_words)
            if not meaningful:
                Logger.debug('meaningful key words none')
                return
            Logger.info('meaningful:', meaningful)
            
            if rawLocation: 
                key_location = rawLocation.split(',')
                latitude = float(key_location[0])
                longitude = float(key_location[1])
                Logger.info('Latitude: ' + latitude + ', Longitude: ' + longitude)
            else:
                latitude = None
                longitude = None
                Logger.info('No location info in search')
            
            face_name = Utils.get_human_names(rawTag)
            Logger.info('face name:', face_name)
            face_id = list(MongoHelper.get_similar_persons(user_id,face_name))  
            Logger.info('Similar person face id:', str(face_id))
            if face_id :
                meaningful.extend(face_id)
                Logger.info('meaningful_add_face_id:', str(meaningful))
            Logger.debug("before cv: " + str(key_words))
            object_name = Utils.get_object_keywords(key_words)
            Logger.debug("before cv: " + str(object_name))
            cv_tags = Utils.translate_tags(object_name)
            Logger.debug("after cv: " + str(cv_tags))
            if cv_tags:
                meaningful.extend(cv_tags)
                Logger.debug('meaningful_add_cv_tag:', meaningful)
            
            processed_time = NLPTimeConvertor.time_api(rawTag, user_id)
            Logger.debug('time api return:', str(processed_time))
            
            image = []
            if processed_time[0]:
                image = Utils.get_image_by_time(user_id, processed_time[0])
            if processed_time[1]:
                meaningful.extend(processed_time[1])
                image = Utils.get_images_by_tag(user_id, meaningful, image)
            image = Utils.sort_by_location(user_id, latitude, longitude, image)

            Logger.info('returned image:',image)    
            result['status'] = True
            result['image'] = image
            Logger.debug('result: ' + str(result))


        finally:
            self.write(json.dumps(result))
