#Encoding=UTF8

import json
from src import BaseAuthenticateHandler
from src import Utils
from src import MongoHelper

class UploadHandler(BaseAuthenticateHandler.BaseAuthenticateHandler):   
    def do_post(self):
        result = {'status': False}
        try:
            userId = self.get_argument('user_id', '')
            latitude = self.get_argument('lat', '')
            longitude = self.get_argument('lon', '')
            desc = self.get_argument('desc', '')
            time = self.get_argument('time', '')
            path = Utils.get_user_path(userId)
            files = self.request.files['image']
            if files is None or len(files) == 0:
                return
            
            fileinfo = files[0]
            fname = fileinfo['filename']
            fh = open(path + "/" + fname, 'wb')
            fh.write(fileinfo['body'])
            result['status'] = True
            
            image = {'user_id': userId, 'image_name': fname, 'lat': float(latitude), 'lon': float(longitude), 'desc': desc, 'time':time, 'processed': False}
            MongoHelper.save_image(image)
        finally:
            self.write(json.dumps(result))
        
        
