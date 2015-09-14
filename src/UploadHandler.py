

import json
import BaseAuthenticateHandler
import Utils
import MongoHelper
import Logger
from datetime import datetime
import FaceUtils


class UploadHandler(BaseAuthenticateHandler.BaseAuthenticateHandler):   
    def do_post(self):
        result = {'status': False}
        Logger.debug('in upload')
        try:
            userId = self.get_argument('user_id', '')
            rawLocation = self.get_argument('loc','')   #add           
            desc = [self.get_argument('tag', '')]
            rawTags = self.get_argument('tag', '')
            rowTime = self.get_argument('time', '')
            faceInfo = self.get_argument('face', '')
            
            token = self.get_argument('token','')           #add
            image_name = self.get_argument('image_name','')    #add
            print('image_name:',image_name)
           
            user = MongoHelper.get_user_by_id(userId)
            if token != user['token']:      #add
                Logger.debug('token wrong')
                return

            print('userId',userId)
            print('rawTags',rawTags)
            
            try:
                path = Utils.get_user_path(userId)    
                        #if self.request.files:
                files = self.request.files['image']
                        # process image file
                if files is None or len(files) == 0:
                    self.write(json.dumps(result))
                    return
                fileinfo = files[0]
                fname = fileinfo['filename']    
                fh = open(path + "/" + fname, 'wb')
                fh.write(fileinfo['body'])
            finally:
                if not MongoHelper.check_img_exist(userId, image_name):
                    if faceInfo is not '':
                        face = faceInfo.split(' ')
                        face_final = FaceUtils.get_face_final(face)
                            # filter out meaningful tags
                    key_words = rawTags.split(' ')
                    print('key_words:',key_words)
                    tags = []
                    if key_words is not None and len(key_words) != 0:
                        tags = Utils.get_meaningful_keywords(key_words)
                        print('tags:',tags)
                            # split date and time
                    temptime = datetime.strptime(rowTime, '%Y-%m-%d %X %z')
                    time = datetime(temptime.year, temptime.month, temptime.day, temptime.hour, temptime.minute, temptime.second, 17100)
                                
                                
                    key_location = rawLocation.split(',') # '1122, 234, beijing, zhongguan'
                    Logger.debug('key_location: ' + str(key_location))
                    raw_location_tag = []
                    if key_location is not None and len(key_location) > 1:
                        location = Utils.get_location_from_rawlocation(key_location)
                        Logger.debug('location: ' + str(location))
                        raw_location_tag = Utils.get_tag_from_rawlocation(key_location)
                        Logger.debug('raw_location_tag: ' + str(raw_location_tag))
                        tags.extend(raw_location_tag)
                        Logger.debug('tags: ' + str(tags))
                                
                            
                    image = {'user_id': userId, 'image_name': fname, 'location':location, 'desc': desc, 'tags': tags, 'time':time, 'processed': False,'face':face_final}
                    MongoHelper.save_image(image)
                    Utils.update_time_indexer(userId,image)
                else:   ##图片上传过，则为更新tag或face
                    if faceInfo is not '':
                        face = faceInfo.split(' ')
                        face_final = FaceUtils.get_face_final(face)
                        MongoHelper.update_face_in_existimage(userId,image_name,face_final)
                    Utils.update_image_tag(rawTags,userId,image_name)
                    
                    
                result['status'] = True           
        finally:
            self.write(json.dumps(result))
            

                
    
         
      
# if __name__ == "__main__":
#     