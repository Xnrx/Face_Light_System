import threading

class ThreadManager:
    def __init__(self):
        """
        初始化ThreadManager类的新实例。
        """
        self.threads = []

    def add_thread(self, target, args=()):
        """
        创建一个新线程并将其添加到线程列表中。
        :param target: 线程要执行的目标函数。
        :param args: 目标函数的参数。
        """
        thread = threading.Thread(target=target, args=args)
        self.threads.append(thread)

    def start_all_threads(self):
        """
        启动线程列表中的所有线程。
        """
        lock = threading.Lock()
        for thread in self.threads:
            with lock:
                thread.start()

    def join_all_threads(self):
        """
        等待线程列表中的所有线程完成。
        """
        for thread in self.threads:
            thread.join()
