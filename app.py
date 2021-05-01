import tornado.ioloop
import tornado.web
from pywebio.platform.tornado import webio_handler
from tornado.options import define, options

from src.markdown import markdown
from src.todolist import todolist

define('port', default=8080, help='Run on the given port', type=int)
define('debug', default=False, help='Run on the debug mode', type=bool)


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")


class FourOhFourHandler(tornado.web.RequestHandler):
    def get(self, slug):
        self.render('src/404.html')


if __name__ == '__main__':
    tornado.options.parse_command_line()

    tornado_settings = {'debug': options.debug}

    application = tornado.web.Application([
        (r'/', webio_handler(todolist)),
        (r'/hello', HelloHandler),
        (r'/markdown', webio_handler(markdown)),
        (r'/([^/]+)', FourOhFourHandler),
    ], **tornado_settings)

    application.listen(port=options.port)
    tornado.ioloop.IOLoop.current().start()
