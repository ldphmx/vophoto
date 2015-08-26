#Encoding=UTF8

import json
from src import BaseAuthenticateHandler
from src import Utils
from src import MongoHelper
from src.MongoHelper import check_img_exist
from datetime import datetime

class UploadHandler(BaseAuthenticateHandler.BaseAuthenticateHandler):   
    def do_post(self):
        result = {'status': False}
        try:
            userId = self.get_argument('user_id', '')
            rawLocation = self.get_argument('loc','')
            desc = self.get_argument('desc', '')
            rawTags = self.get_argument('tag', '')
            rowTime = self.get_argument('time', '')
            clientLocation = self.get_argument('clocat','')  #add by peigang
            token = self.get_argument('token','')
            user = MongoHelper.get_user_by_id(userId)
            if token != user['token']:
                return
        
            path = Utils.get_user_path(userId)
            files = self.request.files['image']
            
            # process image file
            if files is None or len(files) == 0:
                self.write(json.dumps(result))
                return
            fileinfo = files[0]
            fname = fileinfo['filename']
           
            ###for images that has uploaded:if this image was existed,then the customer just want to extend image-tags###
            if check_img_exist(userId, fname):
                key_words = rawTags.split(' ')
                tags = Utils.get_meaningful_keywords(key_words)
                MongoHelper.extend_tags_in_existimage(userId,fname,tags)
                result['status'] = True
            ###for images that has not uploaded###    
            else:
                fh = open(path + "/" + fname, 'wb')
                fh.write(fileinfo['body'])
            
            # filter out meaningful tags
                key_words = rawTags.split(' ')
                if key_words is None or len(key_words) == 0:
                    return
                tags = Utils.get_meaningful_keywords(key_words)
            
            
            # split date and time
                time = datetime.strptime(rowTime, '%Y-%m-%d %X %z')
            
            
                key_location = rawLocation.split(',')               #add         
                if key_location is None or len(key_location) == 0:
                    return
                location = Utils.get_location_from_rawlocation(key_location)
                raw_location_tag = Utils.get_tag_from_rawlocation(key_location)
                tags.extend(raw_location_tag)
            
                image = {'user_id': userId, 'image_name': fname, 'client_loc': clientLocation,'location':location, 'desc': desc, 'tags': tags, 'time':time, 'processed': False}
                MongoHelper.save_image(image)
                result['status'] = True
        finally:
            self.write(json.dumps(result))
        
        
