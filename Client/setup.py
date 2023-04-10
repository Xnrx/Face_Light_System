import sys

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets

from CameraSelector import CameraSelector
from UI_MainWindow3 import Ui__MainWindow


class MainWindow(Ui__MainWindow, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.image = None
        self.timer_camera = QtCore.QTimer()  # 定义定时器，用于控制显示视频的帧率
        self.camera_index = 0
        self.url = 'http://172.20.10.2/cam-hi.jpg'  # 改成自己的ip地址+/cam-hi.jpg
        self.caS = CameraSelector('ip', self.camera_index, self.url)
        self.cap = self.caS.camera  # 视频流
        self.setupUi(self)
        self.slot_init()  # 初始化槽函数

    def slot_init(self):
        """初始化所有槽函数"""
        self.button_open_camera.clicked.connect(self.button_open_camera_clicked)  # 若该按键被点击，则调用button_open_camera_clicked()
        self.timer_camera.timeout.connect(self.show_camera)  # 若定时器结束，则调用show_camera()
        self.button_close.clicked.connect(self.close)  # 若该按键被点击 ，则调用close()，注意这个close是父类QtWidgets.QWidget自带的，会关闭程序

    def button_open_camera_clicked(self):
        """槽函数之一"""
        if not self.timer_camera.isActive():  # 若定时器未启动
            if self.caS.get_camera_type() == 'local':
                self.cap.capture.open(self.camera_index)
            self.timer_camera.start(30)  # 定时器开始计时30ms，结果是每过30ms从摄像头中取一帧显示
            self.button_open_camera.setText('关闭摄像头')

        else:
            self.timer_camera.stop()  # 关闭定时器
            self.cap.release()  # 释放视频流
            self.label_show_camera.clear()  # 清空视频显示区域
            self.button_open_camera.setText('打开摄像头')

    def show_camera(self):
        self.image = self.cap.get_frame()
        show = cv2.resize(self.image, (896, 672))  # 把读到的帧的大小重新设置为 640x480
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 固定的，表示程序应用
    ui = MainWindow()  # 实例化Ui_MainWindow
    ui.show()  # 调用ui的show()以显示。同样show()是源于父类QtWidgets.QWidget的
    sys.exit(app.exec_())  # 不加这句，程序界面会一闪而过
