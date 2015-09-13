#Encoding=UTF8

import tornado.ioloop
import tornado.web
import RegistryHandler
import LoginHandler
import UploadHandler
import SearchHandler
import PaymentHandler

application = tornado.web.Application([
    (r"/register", RegistryHandler.RegistryHandler),
    (r"/login", LoginHandler.LoginHandler),
    (r"/upload", UploadHandler.UploadHandler),
    (r"/search", SearchHandler.SearchHandler),
    (r"/payment", PaymentHandler.PaymentHandler)
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()