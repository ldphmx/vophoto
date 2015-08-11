#Encoding=UTF8

import tornado.web
import MongoHelper
import json
import Utils

class BaseAuthenticateHandler(tornado.web.RequestHandler):
    def get(self):
        if self.isValid():
            self.doGet()
        else:
            self.outputError()
        
    
    def isValid(self):
        if self.pass_auth():
            return True
        
        result = False
        token = self.get_argument('token', '')
        user_id = self.get_argument('userId', '')
        if token == '' or token != Utils.generate_access_token(user_id):
            return False
        else:
            return True
        
    def outputError(self):
        self.write({'status:': False})
    
    def post(self):
        if self.isValid():
            self.doPost()
        else:
            self.outputError()
          
    def pass_auth(self):
        return False
      
    def doGet(self):
        pass
    
    def doPost(self):
        pass