#Encoding=UTF8

import tornado.ioloop
import tornado.web
import RegistryHandler
import LoginHandler
import UploadHandler

application = tornado.web.Application([
    (r"/register", RegistryHandler.RegistryHandler),
    (r"/login", LoginHandler.LoginHandler),
    (r"/upload", UploadHandler.UploadHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()