import sys

import cv2
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog

from UpdateUI import Ui_Update_User_Dialog


class UpdateWindowThread(QThread):
    update_window_closed = pyqtSignal()

    def __init__(self, Sys, img, user_name):
        """
        初始化添加窗口的线程实例
        :param img: 要传进去的图像
        :param Sys: 人脸识别系统
        :param user_name: user_name
        """
        super(UpdateWindowThread, self).__init__()
        self.update_window = UpdateWindow(Sys, img, user_name)  # 初始化窗口ui
        # 转格式
        show = cv2.resize(img, (896, 672))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.update_window.label_face_img.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.update_window.exec_()

    def run(self):
        self.update_window_closed.emit()


class UpdateWindow(QDialog, Ui_Update_User_Dialog):
    def __init__(self, Sys, img, user_name):
        super().__init__()
        self.setupUi(self, Sys, img, user_name)

    def closeEvent(self, event):
        if event.isAccepted():
            # 执行你想要的代码
            print("关闭事件被接受")
        event.accept()

