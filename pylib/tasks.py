from celery import Celery
from celery.schedules import crontab

from pylib import count_down

app = Celery('tasks', broker='amqp://guest@localhost//')
app.conf.beat_schedule = {
    'add-every-minute': {
        'task': 'tasks.test',
        'schedule': crontab(minute='*/1'),
        'args': (5),
    },
}

@app.task
def test(timeout=5):
    return count_down(timeout)

if __name__ == '__main__':
    print test.delay()
