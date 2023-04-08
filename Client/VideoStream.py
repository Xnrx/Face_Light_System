import cv2
from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow
from CameraSelector import CameraSelector
from FrameProcessor import FrameProcessor


class VideoStream(QMainWindow, QThread):
    def __init__(self, UI):
        """
        初始化VideoStream类实例
        :param UI: 应用界面
        """
        super().__init__()
        self.frame = None
        self.ui = UI
        # 视频模块
        url = 'http://172.20.10.2/cam-hi.jpg'
        self.camera_index = 0
        self.camera_select = CameraSelector('local', self.camera_index, url)
        self.camera = self.camera_select.camera
        # 延时
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(1000 // 30)  # 每秒更新30次
        # 处理图像
        self.frame_processor = FrameProcessor(self.ui)

    def run(self):
        """
        更新图像帧
        """
        frame = self.camera.get_frame()
        frame = cv2.resize(frame, (960, 720))
        self.frame_processor.process_frame(frame)
        # 将OpenCV的BGR图像转换为RGB图像，并转换为QImage格式
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = rgb_image.shape
        q_image = QImage(rgb_image.data, w, h, w * c, QImage.Format_RGB888)
        # 将QImage转换为QPixmap，并设置到QLabel上显示
        self.ui.video.setPixmap(QPixmap.fromImage(q_image))

