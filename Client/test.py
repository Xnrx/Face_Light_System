import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot, QByteArray, QDataStream


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class MyThread(QThread):
    data_received = pyqtSignal(User)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.user = User("Alice", 18)

    def run(self):
        time.sleep(1)  # 模拟一些计算密集型的操作
        self.data_received.emit(self.user)


class MyObject(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread = MyThread(self)
        self.thread.data_received.connect(self.handle_data)

    def start_thread(self):
        self.thread.start()

    @pyqtSlot(User)
    def handle_data(self, user):
        print(f"Received data from thread: {user.name}, {user.age}")


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    obj = MyObject()
    obj.start_thread()

    sys.exit(app.exec_())
