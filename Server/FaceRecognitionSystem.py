import cv2  # 导入OpenCV库。
from FaceRecognizer import FaceRecognizer  # 导入FaceRecognizer类。
from ArduinoController import ArduinoController  # 导入ArduinoController类。
from User import User


class FaceRecognitionSystem(FaceRecognizer, ArduinoController):
    def __init__(self, modelD_path, modelR_path, input_shape, port, rate, user_list):
        """
        初始化FaceRecognitionSystem类的新实例。
        :param modelD_path: 人脸检测模型文件的路径。
        :param modelR_path: 人脸识别模型文件的路径。
        :param input_shape: 图像文件的统一尺寸。
        :param port: Arduino板所连接的串行端口。
        :param rate: Arduino串口通信波特率。
        :param user_list: 用户列表。
        """
        FaceRecognizer.__init__(self, modelD_path, modelR_path, input_shape)  # 调用FaceRecognizer类的构造函数
        ArduinoController.__init__(self, port, rate)  # 调用ArduinoController类的构造函数
        self.cosine_similarity_threshold = 0.363  # 余弦相似度阈值
        self.l2_similarity_threshold = 1.128  # L2范数相似度阈值
        self.user_list = user_list  # 用户列表
        self.last_signal = None

    def recognize_user(self, image):
        """
        识别图像中的人脸最符合哪个用户。
        :param image: 要识别的人脸的图像。
        :return: 最符合的用户。
        """
        best_match_user = User('未登记人员', '255000000')  # 最相似的用户。
        best_match_score = -1  # 最高的相似度得分。

        feature1 = self.recognize_face(image)  # 提取要识别的人脸的特征向量。

        if feature1 is None:
            best_match_user = User('未检测到人脸', '255000000')
        else:
            for user in self.user_list:  # 遍历用户列表。
                for feature2 in user.features:  # 遍历当前用户的特征向量列表。
                    similarity_cosine = self.recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)  # 计算余弦相似度得分。
                    similarity_l2 = self.recognizer.match(feature1, feature2, cv2.FaceRecognizerSF_FR_NORM_L2)  # 计算L2范数相似度得分。
                    if similarity_cosine >= self.cosine_similarity_threshold or similarity_l2 <= self.l2_similarity_threshold:  # 如果相似度得分大于阈值。
                        if similarity_cosine > best_match_score:  # 如果余弦相似度得分大于最高得分。
                            best_match_user = user  # 将当前用户设置为最相似的用户。
                            best_match_score = similarity_cosine  # 将当前余弦相似度得分设置为最高得分。

        return best_match_user  # 返回最相似的用户。

    def set_user_lists(self, lists):
        """
        更新用户列表
        :param lists: 用户列表
        """
        self.user_list = lists

    def receive_and_send_signal(self, cur_user):
        """
        收发信号
        :param cur_user: 当前用户id
        """
        signal = cur_user.RGB
        if self.serial.in_waiting:
            self.send_signal(signal)
            self.receive_signal('utf-8')


