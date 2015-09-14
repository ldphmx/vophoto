#Encoding=UTF8

import tornado.web
import MongoHelper
import json
import Utils
import Logger

class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        result = {'status': False}
        Logger.debug('in login')
        try:
            user_id = self.get_argument('user_name', '')
            password = self.get_argument('password', '')
            Logger.info('userid: ' + user_id + ', pass:' + password)
            
            if user_id == '' or password == '':
                Logger.debug('user id null')
                return
            
            user = MongoHelper.get_user(user_id, password)
            if user is None:
                Logger.debug('user none')
                return
            
            result['token'] = Utils.generate_access_token(user_id)
            user_token = result['token']
            MongoHelper.update_user_token(user_id, user_token)
            
            login_time = Utils.get_login_time(user_id)
            img_quota = Utils.get_img_quota(user_id, login_time)
            result['login_time'] = login_time
            result['img_quota'] = img_quota
            result['status'] = True
                
        finally:
            self.write(json.dumps(result))
