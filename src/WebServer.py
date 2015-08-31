#Encoding=UTF8

import tornado.ioloop
import tornado.web
from src import RegistryHandler
from src import LoginHandler
from src import UploadHandler
from src import SearchHandler

application = tornado.web.Application([
    (r"/register", RegistryHandler.RegistryHandler),
    (r"/login", LoginHandler.LoginHandler),
    (r"/upload", UploadHandler.UploadHandler),
    (r"/search", SearchHandler.SearchHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()