#Encoding=UTF8

from xpinyin import Pinyin

config = {
    'access_token': 'secret',
    'mongo_host':'localhost',
    'photo_root': 'E:/data/photos/',
    'servers': [{'name' : 'localhost', 'capacity': 100}],
    'image_process_batch': 10,
    'meaningful_pos':['ns','nt','n'],
    'human_name_pos':['nh'],
    'memcached_url': '127.0.0.1:11211',
    'face_api_key':'842282b7109d49b1914b0541cb6b1ad5'
}