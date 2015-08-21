#Encoding=UTF8

import tornado.web
from src import MongoHelper
import json
from src import Utils
from src import BaseAuthenticateHandler

class SearchHandler(BaseAuthenticateHandler.BaseAuthenticateHandler):
    def post(self):
        result = {'status': False}
        try:
            user_id = self.get_argument('user_id', '')
            raw = self.get_argument('raw', '')
            # 我_r 想_v 找_v 去年_nt 夏天_nt 在_p 西雅图_ns 农贸市场_n 的_u 照片_n
            
            if user_id == '' or raw == '':
                return
            
            key_words = raw.split(' ')
            if key_words is None or len(key_words) == 0:
                return
            
            meaningful = Utils.get_meaningful_keywords(key_words)
            
            
        finally:
            self.write(json.dumps(result))