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
            latitude = self.get_argument('lat', '')
            longitude = self.get_argument('lon', '')
            desc = self.get_argument('desc', '')
            rawTags = self.get_argument('tag', '')
            rowTime = self.get_argument('time', '')
        ######added by peigang###
            token = self.get_argument('token','')
            user = MongoHelper.get_user_by_id(userId)
            if token != user['token']:
                return
        ######added by peigang###
            path = Utils.get_user_path(userId)
            files = self.request.files['image']
            
            # process image file
            if files is None or len(files) == 0:
                self.write(json.dumps(result))
                return
            fileinfo = files[0]
            fname = fileinfo['filename']
            if check_img_exist(userId, fname):
                self.write(json.dumps(result))
                return
            fh = open(path + "/" + fname, 'wb')
            fh.write(fileinfo['body'])
            
            # filter out meaningful tags
            key_words = rawTags.split(' ')
            if key_words is None or len(key_words) == 0:
                return
            tags = Utils.get_meaningful_keywords(key_words)
            
            # split date and time
            time = datetime.strptime(rowTime, '%Y-%m-%d %X %z')
            
            image = {'user_id': userId, 'image_name': fname, 'lat': float(latitude), 'lon': float(longitude), 'desc': desc, 'tags': tags, 'time':time, 'processed': False}
            MongoHelper.save_image(image)
            result['status'] = True
        finally:
            self.write(json.dumps(result))
        
        
