import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog

from DeleteUI import Ui_Dialog


class DeleteWindowThread(QThread):
    delete_window_closed = pyqtSignal()

    def __init__(self, Sys, user_name):
        """
        初始化添加窗口的线程实例
        :param user_name: 用户名
        :param Sys: 人脸识别系统
        """
        super(DeleteWindowThread, self).__init__()
        self.delete_window = DeleteWindow(Sys, user_name)  # 初始化窗口ui
        self.delete_window.exec_()

    def run(self):
        self.delete_window_closed.emit()


class DeleteWindow(QDialog, Ui_Dialog):
    def __init__(self, Sys, user_name):
        super().__init__()
        self.setupUi(self, Sys, user_name)

    def closeEvent(self, event):
        if event.isAccepted():
            # 执行你想要的代码
            print("关闭事件被接受")
        event.accept()