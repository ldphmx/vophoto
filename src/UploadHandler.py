#Encoding=UTF8

import json
from src import BaseAuthenticateHandler
from src import Utils
from src import MongoHelper
# from src.MongoHelper import check_img_exist
from datetime import datetime

class UploadHandler(BaseAuthenticateHandler.BaseAuthenticateHandler):   
    def do_post(self):
        result = {'status': False}
        try:
            userId = self.get_argument('user_id', '')
            rawLocation = self.get_argument('loc','')   #add           
            desc = self.get_argument('desc', '')
            rawTags = self.get_argument('tag', '')
            rowTime = self.get_argument('time', '')
            function = self.get_argument('func','')  #
            token = self.get_argument('token','')           #add
            image_name = self.get_argument('image_name','')    #add
            user = MongoHelper.get_user_by_id(userId)
            if token != user['token']:      #add
                return
            ###for images that has uploaded:if this image was existed,then the customer just want to extend image-tags###
            if function == 'UPDATE':
                update_image_tag(rawTags,userId,image_name)
                face_name = Utils.get_human_names(rawTags)
                if face_name is not None:
                    MongoHelper.update_facename_in_person_list(face_name)
                result['status'] = True
            
            elif function == 'UPLOAD':    ###for images that has not uploaded###    
                
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
            # filter out meaningful tags
                key_words = rawTags.split(' ')
                tags = []
                if key_words is not None and len(key_words) != 0:
                    tags = Utils.get_meaningful_keywords(key_words)
            # split date and time
                time = datetime.strptime(rowTime, '%Y-%m-%d %X %z')
                key_location = rawLocation.split(',')               #add         
                raw_location_tag = []
                if key_location is not None and len(key_location) != 0:
                    location = Utils.get_location_from_rawlocation(key_location)
                    raw_location_tag = Utils.get_tag_from_rawlocation(key_location)
                    tags.extend(raw_location_tag)
            
                image = {'user_id': userId, 'image_name': fname, 'location':location, 'desc': desc, 'tags': tags, 'time':time, 'processed': False}
                MongoHelper.save_image(image)
                face_name = Utils.get_human_names(rawTags)
                MongoHelper.update_person_list(userId,face_name)        ##此函数未写
                result['status'] = True
        finally:
            self.write(json.dumps(result))
            
def update_image_tag(rawTags,userId,image_name):
                key_words = rawTags.split(' ')
                tags = Utils.get_meaningful_keywords(key_words)
                MongoHelper.extend_tags_in_existimage(userId,image_name,tags)
