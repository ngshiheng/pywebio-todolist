
from functools import partial

from pywebio.input import TEXT, input
from pywebio.output import clear, put_buttons, put_html, put_table, put_text, use_scope
from pywebio.platform.utils import seo


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
                '🤩 Your Awesome Tasks',
                '✅ Have you completed your task?',
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
                    '🤩 Your Awesome Tasks',
                    '✅ Have you completed your task?',
                ],
            )
