"""
that module contains many tasks which shall do something...
for example
- we ping web resources which were configured
- we do health check of agents (if it necessary)
"""

import subprocess
import time
import unittest
from datetime import timedelta
from multiprocessing import Process

import requests
from celery import Celery
from celery.task import periodic_task
from celery import current_app
from celery.bin import worker

from pylib import count_down

app = Celery('tasks', broker='amqp://guest@localhost//')

def run_celery_server():
    # celery worker -l debug -A tasks --beat
    application = current_app._get_current_object()
    worker_process = worker.worker(app=application)
    options = {
        'broker': 'amqp://super@localhost//',
        'loglevel': 'INFO',
        'traceback': False,
    }
    worker_process.run(**options)

@app.task
def test_task(timeout=5):
    return count_down(timeout)

@periodic_task(run_every=timedelta(seconds=5))
def ping_web(url='http://google.com'):
    res = requests.get(url, timeout=3)
    return res


class TestTasks(unittest.TestCase):
    celery_server = None

    @classmethod
    def setUpClass(cls):
        cls.celery_server = Process(target=run_celery_server)
        cls.celery_server.start()
        time.sleep(4)
        print "Celery pid={}".format(cls.celery_server.pid)

    @classmethod
    def tearDownClass(cls):
        time.sleep(10)
        cls.celery_server.terminate()

    def test_nothing(self):
        time.sleep(2)

if __name__ == '__main__':
    #unittest.main(verbosity=True)
    run_celery_server()









