import cv2
from PyQt5 import QtCore, QtGui

from CameraSelector import CameraSelector


class CameraThread(QtCore.QThread):
    # 信号
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
        self.caS = CameraSelector('ip', self.camera_index, self.url)  # 选择摄像头
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