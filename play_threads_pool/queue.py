import threading
import time


class NotCapacityException:
    pass


class ParameterException:
    pass


class ThreadSafeQueue(object):

    def __init__(self, capacity=0):
        self.queue = []
        self.capacity = capacity
        self.lock = threading.Lock()
        self.condition = threading.Condition()

    def size(self):
        self.lock.acquire()
        size = len(self.queue)
        self.lock.release()
        return size

    def add(self, item):
        if self.capacity != 0 and self.size() > self.capacity:
            return NotCapacityException()

        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()

    def add_list(self, item_list):
        if not isinstance(item_list, list):
            item_list = list(item_list)

        for item in item_list:
            self.add(item)

    def remove(self, block=False, timeout=0):
        if self.size() == 0:
            if block:
                self.condition.acquire()
                self.condition.wait(timeout=timeout)
                self.condition.release()
            else:
                return None

        self.lock.acquire()

        item = None
        if len(self.queue) > 0:
            item = self.queue.pop()

        self.lock.release()
        return item

    def get(self, index):
        if self.size() == 0:
            return None
        if index >= self.size() or index < 0:
            return ParameterException()
        self.lock.acquire()
        item = self.queue[index]
        self.lock.release()
        return item
