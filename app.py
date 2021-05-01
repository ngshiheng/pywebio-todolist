from functools import partial

import tornado.ioloop
import tornado.web
from pywebio.input import TEXT, input
from pywebio.output import clear, put_buttons, put_html, put_table, put_text, use_scope
from pywebio.platform.tornado import webio_handler
from pywebio.platform.utils import seo
from tornado.options import define, options

define('port', default=8080, help='Run on the given port', type=int)
define('debug', default=False, help='Run on the debug mode', type=bool)


def complete_task(choice: str, task: str, tasks):
    if choice == 'Complete':
        tasks.remove(task)

    clear('tasks')
    if tasks:
        put_table(
            tdata=[
                [
                    put_text(task),
                    put_buttons(['Complete'], onclick=partial(complete_task, task=task, tasks=tasks))
                ] for task in tasks
            ],
            header=[
                'Your Tasks',
                'Actions',
            ],
            scope='tasks',
        )


@seo('To-Do List', 'A to-do list made using PyWebIO.')
def todolist():
    tasks = []

    put_html(r"""<h1 align="center"><strong>📝 To-Do List</strong></h1>""")
    with use_scope('tasks'):
        while True:
            task = input(
                type=TEXT,
                required=True,
                label='🏃 What are you going to do today?',
                placeholder='Add a task...',
                help_text='Try: "Write an article"',
            )
            tasks.append(task)

            clear('tasks')
            put_table(
                tdata=[
                    [
                        task,
                        put_buttons(['Complete'], onclick=partial(complete_task, task=task, tasks=tasks))
                    ] for task in tasks
                ],
                header=[
                    'Tasks',
                    'Status',
                ],
            )


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!")


if __name__ == '__main__':
    tornado.options.parse_command_line()

    tornado_settings = {'debug': options.debug}

    application = tornado.web.Application([
        (r'/about', MainHandler),
        (r'/todolist', webio_handler(todolist)),
    ], **tornado_settings)

    application.listen(port=options.port)
    tornado.ioloop.IOLoop.current().start()
