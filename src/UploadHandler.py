

import json
from src import BaseAuthenticateHandler
from src import Utils
from src import MongoHelper
from src import Logger
from datetime import datetime
import pypinyin


class UploadHandler(BaseAuthenticateHandler.BaseAuthenticateHandler):   
    def do_post(self):
        result = {'status': False}
        Logger.debug('in upload')
        try:
            userId = self.get_argument('user_id', '')
<<<<<<< HEAD
            rawLocation = self.get_argument('loc','')   #add           
            desc = self.get_argument('tag', '')
=======
            rawLocation = self.get_argument('loc','')   
            desc = [pypinyin.slug(self.get_argument('desc', ''))]
>>>>>>> dee034f50937a3f345c6b495e8c04a2e919f156b
            rawTags = self.get_argument('tag', '')
            rowTime = self.get_argument('time', '')
            function = self.get_argument('func','')  
            token = self.get_argument('token','')           
            image_name = self.get_argument('image_name','')
            Logger.debug('image_name:' + image_name + ', function: ' + function)
            user = MongoHelper.get_user_by_id(userId)
            if token != user['token']:
                Logger.debug('token value false')
                return
            
            if function == 'UPDATE':
                Logger.info('rawTags: ' + rawTags + ', userId: ' + userId + ', image_name: ' + image_name)
                update_image_tag(rawTags,userId,image_name)
                MongoHelper.update_image_desc_and_status(desc,userId,image_name)  
                result['status'] = True
            
            elif function == 'UPLOAD':
                Logger.info('rawTags: ' + rawTags + ', userId: ' + userId)
                path = Utils.get_user_path(userId)    #error
            #if self.request.files:
                files = self.request.files['image']
            # process image file
                if files is None or len(files) == 0:
                    self.write(json.dumps(result))
                    Logger.debug('file none')
                    return
                fileinfo = files[0]
                fname = fileinfo['filename']    
                fh = open(path + "/" + fname, 'wb')
                fh.write(fileinfo['body'])
            # filter out meaningful tags
                key_words = rawTags.split(' ')
                print('key_words:',key_words)
                tags = []
                if key_words is not None and len(key_words) != 0:
                    tags = Utils.get_meaningful_keywords(key_words)
                    print('tags:',tags)
            # split date and time
                time = datetime.strptime(rowTime, '%Y-%m-%d %X %z')
                
                
                key_location = rawLocation.split(',')               #add         
                print('key_location:',key_location)
                raw_location_tag = []
                if key_location is not None and len(key_location) != 0:
                    location = Utils.get_location_from_rawlocation(key_location)
                    print('location',location)
                    raw_location_tag = Utils.get_tag_from_rawlocation(key_location)
                    print('raw_location_tag',raw_location_tag)
                    tags.extend(raw_location_tag)
                    print('tags',tags)
                
            
                image = {'user_id': userId, 'image_name': fname, 'location':location, 'desc': desc, 'tags': tags, 'time':time, 'processed': False}
                MongoHelper.save_image(image)
                Utils.update_time_indexer(userId,image)
#                 face_name = Utils.get_human_names(rawTags)
#                 MongoHelper.update_person_list(userId,face_name)        ##此函数未写
                result['status'] = True
                Logger.info('upload successfully')
        finally:
            self.write(json.dumps(result))
            
def update_image_tag(rawTags,userId,image_name):
                key_words = rawTags.split(' ')
                print('key_words:',key_words)
                tags = Utils.get_meaningful_keywords(key_words)
                print('tags:',tags)
                MongoHelper.extend_tags_in_existimage(userId,image_name,tags)
                
    
         
      
# if __name__ == "__main__":
#     