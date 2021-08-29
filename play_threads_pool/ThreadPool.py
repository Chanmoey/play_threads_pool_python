import psutil

from play_threads_pool.ProcessThread import ProcessThread
from play_threads_pool.queue import ThreadSafeQueue
from play_threads_pool.task import Task


class NotTaskTypeException:
    pass


class ThreadPool:

    def __init__(self, capacity=0):
        if not capacity:
            capacity = psutil.cpu_count() * 2

        # 线程池
        self.pool = ThreadSafeQueue(capacity)

        # 任务队列
        self.task_queue = ThreadSafeQueue()
        for i in range(capacity):
            self.pool.add(ProcessThread(self.task_queue))

    def start(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.start()

    # 停止线程池
    def join(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.stop()
        while self.pool.size():
            thread = self.pool.remove()
            thread.join()

    def add(self, item):
        if not isinstance(item, Task):
            raise NotTaskTypeException()
        self.task_queue.add(item)

    def add_list(self, item_list):
        if not isinstance(item_list, list):
            item_list = list(item_list)

        for item in item_list:
            self.add(item)

    def size(self):
        return self.pool.size()
