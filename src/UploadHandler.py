#Encoding=UTF8

import json
import BaseAuthenticateHandler
import Utils
import MongoHelper

class UploadHandler(BaseAuthenticateHandler.BaseAuthenticateHandler):   
    def doPost(self):
        result = {'status': False}
        try:
            userId = self.get_argument('userId', '')
            location = self.get_argument('loc', '')
            desc = self.get_argument('desc', '')
            path = Utils.create_user_path(userId)
            files = self.request.files['search']
            if files is None or len(files) == 0:
                return
            
            fileinfo = self.request.files['search'][0]
            fname = fileinfo['filename']
            fh = open(path + "/" + fname, 'wb')
            fh.write(fileinfo['body'])
            result['status'] = True
            
            image = {'image_name': fname, 'loc': location, 'desc': desc}
            MongoHelper.save_image(image)
        finally:
            self.write(json.dumps(result))
        
        