import sys

import cv2
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog

from AddUI import Ui_Add_User_Dialog


class AddWindowThread(QThread):
    add_window_closed = pyqtSignal()

    def __init__(self, img, Sys):
        """
        初始化添加窗口的线程实例
        :param img: 要传进去的图像
        :param Sys: 人脸识别系统
        """
        super(AddWindowThread, self).__init__()
        self.add_window = AddWindow(Sys, img)  # 初始化窗口ui
        # 转格式
        show = cv2.resize(img, (896, 672))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.add_window.label_face_img.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.add_window.exec_()

    def run(self):
        self.add_window_closed.emit()


class AddWindow(QDialog, Ui_Add_User_Dialog):
    def __init__(self, Sys, img):
        super().__init__()
        self.setupUi(self, Sys, img)

    def closeEvent(self, event):
        if event.isAccepted():
            # 执行你想要的代码
            print("关闭事件被接受")
        event.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 固定的，表示程序应用
    ui = AddWindow()  # 实例化Ui_MainWindow
    ui.show()  # 调用ui的show()以显示。同样show()是源于父类QtWidgets.QWidget的
    sys.exit(app.exec_())  # 不加这句，程序界面会一闪而过
