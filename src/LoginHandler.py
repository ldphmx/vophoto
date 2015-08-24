#Encoding=UTF8

import tornado.web
import MongoHelper
import json
import Utils

class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        result = {'status': False}
        try:
            user_id = self.get_argument('user_id', '')
            password = self.get_argument('password', '')
            
            if user_id == '' or password == '':
                return
            
            user = MongoHelper.get_user(user_id, password)
            if user is None:
                return
            else:
                result['status'] = True
            ###    result['user'] = user   ###
                result['token'] = Utils.generate_access_token(user_id)
                ###added by peigang###
                user['token'] = result['token']
                ###added by peigang###
        finally:
            self.write(json.dumps(result))
