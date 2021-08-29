import threading

from play_threads_pool.task import Task, AsyncTask


class ProcessThread(threading.Thread):

    def __init__(self, task_queue, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)

        # 线程停止的标记
        self.dismiss_flag = threading.Event()

        self.task_queue = task_queue
        self.args = args
        self.kwargs = kwargs

    def run(self):
        while True:

            if self.dismiss_flag.is_set():
                break

            task = self.task_queue.remove()
            if not isinstance(task, Task):
                continue

            # 执行传入到task中的函数逻辑
            result = task.callable(*task.args, **task.kwargs)
            if isinstance(task, AsyncTask):
                task.set_result(result)

    def dismiss(self):
        self.dismiss_flag.set()

    def stop(self):
        self.dismiss()
