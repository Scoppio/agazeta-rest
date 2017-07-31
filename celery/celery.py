
from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('tasks',
             broker='redis://localhost')

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()


@app.task
def add(x, y):
    return x + y