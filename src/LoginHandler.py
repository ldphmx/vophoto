#Encoding=UTF8

import tornado.web
from src import MongoHelper
import json
from src import Utils

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
                user_token = result['token']
                MongoHelper.update_user_token(user_id,user_token)     #update
                ###added by peigang###
        finally:
            self.write(json.dumps(result))
