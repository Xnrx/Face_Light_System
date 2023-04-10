from ArduinoController import ArduinoController
from Database import Database
from FaceRecognitionSystem import FaceRecognitionSystem
from FaceRecognizer import FaceRecognizer
from UserManager import UserManager


class InitRecognizerSys(FaceRecognizer, ArduinoController):
    def __init__(self):
        """
        初始化InitRecognizerSys类实例
        """
        self.modelD_path = '../model/face_detection_yunet_2022mar.onnx'
        self.modelR_path = '../model/face_recognition_sface_2021dec.onnx'
        self.input_shape = (300, 300)
        self.port = 'COM7'
        self.rate = 115200
        self.users_path = '../user/'
        self.users_list = []  # 用户列表
        self.faReSys = FaceRecognitionSystem(self.modelD_path, self.modelR_path, self.input_shape, self.port, self.rate, self.users_list)
        self.um = UserManager(self.users_path, self.users_list)  # 用户管理初始化
        self.db = Database(server='LAPTOP-NO19G1TG', user='sa', password='zhong5567', database='Python')  # 数据库初始化
        self.setUsers()

    def setUsers(self):
        """
        用户模块初始化
        """
        self.um.load_images_and_features(self.modelD_path, self.modelR_path, self.input_shape)
        self.db.connect()
        result = self.db.query('SELECT * FROM UserSettings')
        self.um.load_rgbs(result)
