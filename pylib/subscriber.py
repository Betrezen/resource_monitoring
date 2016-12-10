import json
import hashlib
import os
import random
import threading
from multiprocessing import Process, Queue
import time
import unittest

import zmq

from publisher import ZMQPublisher
from settings import LOGGER as logger
from settings import ZEROMQ_SERVER_HOST, ZEROMQ_SERVER_PORT


class ZMQSubscriber(object):
    # multiprocessing Queue
    def __init__(self, queue=None,
                 ip_port='tcp://{}:{}'.format(ZEROMQ_SERVER_HOST, ZEROMQ_SERVER_PORT),
                 msg_filter=['gui', 'all']):
        # logger.debug("ZMQSubscriber init!: ip_port={}".format(ip_port))
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(ip_port)
        self.last_message = None
        self.queue = queue

        for f in msg_filter:
            self.socket.setsockopt(zmq.SUBSCRIBE, f)

        self.stop_sig = threading.Event()
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        # logger.debug('ZMQSubscriber: receive')
        while not self.stop_sig.is_set():
            # logger.debug('ZMQSubscriber: trying to get something')
            try:
                message = self.socket.recv_string(zmq.NOBLOCK)
                logger.debug("ZMQSubscriber: queue={}".format(self.queue))
                if self.queue:
                    self.queue.put(message)
                    # logger.debug("ZMQSubscriber put message to queue. {}".format(message))
                self.last_message = message
                logger.debug("ZMQSubscriber: data={}".format(self.last_message))
            except zmq.ZMQError:
                # logger.debug('ZMQSubscriber: zmq.ZMQError')
                pass
        logger.debug('ZMQSubscriber: Stop')

    def start(self):
        if not self.receive_thread.isAlive():
            self.receive_thread.start()
        self.stop_sig.clear()

    def stop(self):
        self.stop_sig.set()

def init_subscribe(queue, steps=1000):
    try:
        subscriber = ZMQSubscriber(queue=queue)
        while steps > 0:
            if not queue.empty():
                logger.debug('message through queue={}'.format(queue.get()))
            else:
                logger.debug('queue is empty')
                time.sleep(0.2)
            steps -= 1
    except Exception:
        subscriber.stop()
        subscriber.terminate()
        del(subscriber)


def init_publisher():
    publisher = ZMQPublisher()
    i=100
    while i>0:
        barcode = hashlib.sha256(os.urandom(30).encode('base64')[:-1]).hexdigest()[:10]
        publisher.send(barcode, random.choice(['gui', 'all']))
        time.sleep(3)
        i-=1


class TestZMQSubscriber(unittest.TestCase):

    def test_simple(self):
        publisher_process = Process(target=init_publisher)
        publisher_process.start()

        subscriber_queue = Queue()
        subscriber_process = Process(target=init_subscribe, args=(subscriber_queue,))
        subscriber_process.start()

        time.sleep(5)
        publisher_process.terminate()
        subscriber_process.terminate()

    @unittest.skip('opa')
    def test_loop(self):
        publisher = ZMQPublisher()
        subscriber = ZMQSubscriber()
        receivers = ['gui', 'all']
        time.sleep(1)
        count = 0
        while count < 3:
            barcode = hashlib.sha256(os.urandom(30).encode('base64')[:-1]).hexdigest()[:10]
            try:
                receiver = random.choice(receivers)
                publisher.send(barcode, receiver)
                send_message = publisher.last_message
                time.sleep(0.2)
                get_message = subscriber.last_message
                self.assertEqual(get_message, send_message,
                                 'TestZMQSubscriber: seems messages are different')
            except:
                self.assertTrue(False, 'something wrong')

            rnd = random.randint(1, 10)
            print '*'*rnd
            count += 1
            time.sleep(1)
        subscriber.stop()

    @unittest.skip('opa')
    def test_multiprocess(self):
        subscriber_queue = Queue()
        subscriber_process = Process(target=init_subscribe, args=(subscriber_queue,))
        subscriber_process.start()

        publisher_process = Process(target=init_publisher)
        publisher_process.start()

        publisher_process.join()
        subscriber_process.join()

        publisher_process.terminate()
        subscriber_process.terminate()



if __name__ == '__main__':
    unittest.main(verbosity=7)
