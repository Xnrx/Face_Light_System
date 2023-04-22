import sys

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

from AddWindow import AddWindow
from CameraSelector import CameraSelector
from InitRecognizerSys import InitRecognizerSys
from QueryWindow import QueryWindow
from UI__MainWindow import Ui__MainWindow


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


class QueryWindowThread(QThread):
    # 槽
    query_window_closed = pyqtSignal()

    def __init__(self, db):
        """
        初始化查询窗口实例
        :param db: 数据库系统
        """
        super(QueryWindowThread, self).__init__()
        self.query_window = QueryWindow(db)  # 初始化窗口ui
        self.query_window.exec_()
        self.is_running = False

    def run(self):
        """
        线程执行函数
        :return:
        """
        self.query_window_closed.emit()


class CameraThread(QtCore.QThread):
    # 槽
    image_updated = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, camera_index, url, Sys):
        """
        CameraThread线程初始化实例
        :param camera_index: 本地摄像头索引
        :param url: ip摄像头网络地址
        :param Sys: 人脸识别与串口通信系统
        """
        super(CameraThread, self).__init__()
        self.caS = None
        self.camera_index = camera_index
        self.url = url
        self.cap = None
        self.Sys = Sys
        self.faceSys = self.Sys.faReSys
        self.db = self.Sys.db
        self.image = None
        self.user = None
        self.is_running = False

    def run(self):
        """
        线程执行函数
        :return:
        """
        self.caS = CameraSelector('local', self.camera_index, self.url)  # 选择摄像头
        self.cap = self.caS.camera
        if not self.faceSys.serial.isOpen():  # 检测摄像头状态
            self.faceSys.serial.open()
        if self.caS.get_camera_type == 'local':
            self.cap.capture.open(self.camera_index)
        while True:
            if not self.is_running:  # 线程停止运行
                break
            self.image = self.cap.get_frame()
            self.user = self.faceSys.recognize_user(self.image)
            # 将opencv格式图像转化为QImage格式图像
            show = cv2.resize(self.image, (896, 672))
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
            self.image_updated.emit(showImage)  # 转化好的图像格式连接信号槽函数
        self.cap.release()  # 线程停止运行后，关闭摄像头
        # 串口通信终止
        self.faceSys.serial.close()
        self.faceSys.serial.open()
        self.faceSys.serial.close()

    def stop(self):
        """
        线程终止函数
        :return:
        """
        self.is_running = False


class MainWindow(Ui__MainWindow, QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        初始化主窗口实例
        :param parent:
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.Sys = InitRecognizerSys()  # 所有窗口都用这个
        self.faceSys = self.Sys.faReSys
        self.db = self.Sys.db
        self.camera_thread = CameraThread(0, 'http://172.20.10.2/cam-hi.jpg', self.Sys)
        self.slot_init()

    def slot_init(self):
        """
        所有按钮信号槽初始化
        :return:
        """
        self.button_select_user.clicked.connect(self.button_query_user_clicked)
        self.button_close.clicked.connect(self.close)
        self.button_open_camera.clicked.connect(self.button_open_or_close_camera_clicked)
        self.button_add_user.clicked.connect(self.button_add_user_clicked)
        self.button_add_user.setEnabled(False)

    # 添加窗口
    def button_add_user_clicked(self):
        """
        添加窗口按钮打开事件
        在添加窗口打开时关闭camera线程，关闭时打开camera线程，防止线程冲突
        :return:
        """
        # 暂时关闭线程
        self.camera_thread.stop()
        self.camera_thread.image_updated.disconnect(self.update_image_handle_com_and_buttons)  # 槽断开连接信号
        self.label_show_camera.clear()
        self.label_show_id.clear()
        self.button_open_camera.setText('打开摄像头')
        # 添加窗口线程打开
        self.add_thread = AddWindowThread(self.camera_thread.image, self.Sys)
        self.add_thread.add_window_closed.connect(self.on_add_window_closed)
        self.add_thread.start()

    def on_add_window_closed(self):
        """
        添加窗口按钮关闭事件
        :return:
        """
        # 打开线程
        self.camera_thread.image_updated.connect(self.update_image_handle_com_and_buttons)  # 槽连接信号
        self.camera_thread.is_running = True
        self.camera_thread.start()
        self.button_open_camera.setText('关闭摄像头')
        # 添加窗口线程关闭
        self.add_thread.quit()
        self.add_thread.wait()

    def button_query_user_clicked(self):
        """查询窗口按钮打开事件"""
        self.query_thread = QueryWindowThread(self.db)
        self.query_thread.is_running = True
        self.query_thread.query_window_closed.connect(self.on_query_window_closed)
        self.query_thread.start()

    def on_query_window_closed(self):
        """
        查询窗口按钮关闭事件
        :return:
        """
        self.query_thread.is_running = False
        self.query_thread.quit()
        self.query_thread.wait()

    def button_open_or_close_camera_clicked(self):
        """
        打开或关闭摄像头按钮事件
        :return:
        """
        if not self.camera_thread.is_running:
            self.camera_thread.image_updated.connect(self.update_image_handle_com_and_buttons)  # 槽连接信号
            self.camera_thread.is_running = True
            self.camera_thread.start()
            self.button_open_camera.setText('关闭摄像头')
        else:
            self.camera_thread.stop()
            self.camera_thread.image_updated.disconnect(self.update_image_handle_com_and_buttons)  # 槽断开连接信号
            self.label_show_camera.clear()
            self.label_show_id.clear()
            self.button_open_camera.setText('打开摄像头')

    def update_image_handle_com_and_buttons(self, image):
        """
        信号与槽-信号函数
        更新摄像头图像，显示图像id，向arduino发送信号，并处理按钮显示时机
        :param image:camera线程更新的图像
        :return:
        """
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(image))
        self.label_show_id.setText(self.camera_thread.user.user_id)

        # 添加按钮仅当有未登记人员时可用
        if self.camera_thread.user.user_id == '未登记人员':
            self.button_add_user.setEnabled(True)
        else:
            self.button_add_user.setEnabled(False)

        self.faceSys.receive_and_send_signal(self.camera_thread.user)

    def closeEvent(self, event):
        """
        主窗口关闭事件，断开串口通信
        :param event: 关闭事件
        :return:
        """
        # 执行一些代码
        self.faceSys.serial.close()
        self.faceSys.serial.open()
        self.faceSys.serial.close()
        # 调用父类的 closeEvent 方法
        super(MainWindow, self).closeEvent(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 固定的，表示程序应用
    ui = MainWindow()  # 实例化Ui_MainWindow
    ui.show()  # 调用ui的show()以显示。同样show()是源于父类QtWidgets.QWidget的
    sys.exit(app.exec_())  # 不加这句，程序界面会一闪而过
