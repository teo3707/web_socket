# coding: utf-8

import os
import tornado.web
import tornado.wsgi
import tornado.ioloop
import tornado.httpserver
from django.core.wsgi import get_wsgi_application

def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'status_web_socket.settings'

    wsgi_app = get_wsgi_application()
    container = tornado.wsgi.WSGIContainer(wsgi_app)

    from status_web_socket.socket import Socket
    application = tornado.web.Application([
        ('/ws', Socket),
        ('.*', tornado.web.FallbackHandler, dict(fallback=container))
    ])

    server = tornado.httpserver.HTTPServer(application)
    server.listen(8080)
    print('server run on 8080')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()