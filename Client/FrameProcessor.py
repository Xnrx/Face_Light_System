import cv2
from PyQt5.QtCore import pyqtSignal

from Database import Database
from FaceRecognitionSystem import FaceRecognitionSystem
from User import User
from UserManager import UserManager


class FrameProcessor:
    def __init__(self, UI):
        """
        初始化FrameProcessor类实例
        :param UI:应用界面
        """
        self.signal = pyqtSignal(User)
        self.UI = UI
        self.modelD_path = '../model/face_detection_yunet_2022mar.onnx'
        self.modelR_path = '../model/face_recognition_sface_2021dec.onnx'
        self.input_shape = (300, 300)
        self.users_path = '../user/'
        self.users_list = []
        self.port = 'COM7'
        self.rate = 115200
        # 用户管理初始化
        self.um = UserManager(self.users_path, self.users_list)
        self.um.load_images_and_features(self.modelD_path, self.modelR_path, self.input_shape)
        # 人脸识别系统初始化
        self.recognizerSys = FaceRecognitionSystem(self.modelD_path, self.modelR_path, self.input_shape, self.port, self.rate, self.um.list)
        # 数据库初始化
        self.db = Database(server='LAPTOP-NO19G1TG', user='sa', password='zhong5567', database='Python')
        self.db.connect()
        user_datas = self.db.query('SELECT * FROM UserSettings')
        self.um.load_rgbs(user_datas)

    def process_frame(self, frame):
        """
        处理当前帧
        """
        # 在这里处理当前帧并返回结果
        user = self.recognizerSys.recognize_user(frame)
        self.signal.emit(user)
        self.UI.user_name.setText(user.user_id)
