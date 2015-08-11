#Encoding=UTF8

import Config
import md5
import os
import MongoHelper

def get_user_path(userId):
    md5ins = md5.new()
    md5ins.update(userId)
    md5str = md5ins.hexdigest()
    return Config.config['photo_root'] + md5str[0:2] + "/" + md5str[2:4] + "/" + md5str[4:6] + "/" + userId

def create_user_path(userId):
    md5ins = md5.new()
    md5ins.update(userId)
    md5str = md5ins.hexdigest()
    path = Config.config['photo_root'] + md5str[0:2] + "/" + md5str[2:4] + "/" + md5str[4:6] + "/" + userId
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def allocate_user_server(userId):
    servers = Config.config['servers']
    if len(servers) == 0:
        return None
    
    server_usage = MongoHelper.get_server_users()
    for name in server_usage:
        count = server_usage[name]
        capacity = 0
        for server in servers:
            if server['name'] == name:
                capacity = server['capacity']
                break
        
        if count >= capacity:
            continue
        else:
            return name
    
    return None
    
    
def generate_access_token(userId):
    md5ins = md5.new()
    md5ins.update(userId)
    md5ins.update(Config.config['access_token'])
    return md5ins.hexdigest()

if __name__ == "__main__":
    print create_user_path('xxx')