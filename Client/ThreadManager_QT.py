from PyQt5.QtCore import QThread, pyqtSignal


class ThreadManager:
    def __init__(self):
        self.threads = []

    def create_thread(self, target, args=()):
        thread = QThread()
        self.threads.append(thread)

        worker = target(*args)
        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        thread.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        return worker

    def start_all(self):
        for thread in self.threads:
            thread.start()

    def stop_all(self):
        for thread in self.threads:
            thread.quit()
            thread.wait()
