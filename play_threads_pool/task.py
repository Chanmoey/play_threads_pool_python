import threading
import uuid


class Task:

    def __init__(self, func, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.callable = func
        self.id = uuid.uuid4()

    def __str__(self):
        return "Task id: " + str(self.id)


class AsyncTask(Task):

    def __init__(self, func, *args, **kwargs):
        self.result = None
        self.condition = threading.Condition()
        super().__init__(func, *args, **kwargs)

    def set_result(self, result):
        self.condition.acquire()
        self.result = result
        self.condition.notify()
        self.condition.release()

    def get_result(self):
        self.condition.acquire()
        if not self.result:
            self.condition.wait()
        result = self.result
        self.condition.release()
        return result
