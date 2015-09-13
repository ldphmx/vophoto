#Encoding=UTF8

import tornado.web
import MongoHelper
import json
import Utils
import Logger

class PaymentHandler(tornado.web.RequestHandler):
    def post(self):
        result = {'status': False}
        Logger.debug('in payment')
        try:
            user_id = self.get_argument('user_id', '')
            token = self.get_argument('token', '')
            plan = self.get_argument('plan','')
            Logger.info('userid: ' + user_id + ', token:' + token + ', plan:' + plan)
            
            if user_id == '':
                Logger.debug('user id null')
                return
            
            user = MongoHelper.get_user_by_id(user_id)
            if user is None:
                Logger.debug('user none')
                return
            if token is not user['token']:
                self.write(json.dumps(result))
                Logger.debug('token wrong')
                return
            
            result['quota'] = Utils.update_user_payment(user_id, plan)
            result['status'] = True
                
        finally:
            self.write(json.dumps(result))
