import cv2
import numpy as np

from FaceDetector import FaceDetector
from IFaceRecognizer import IFaceRecognizer


class FaceRecognizer(IFaceRecognizer):
    def __init__(self, modelD_path, modelR_path, input_shape):
        """
        初始化FaceRecognizer类的新实例。
        :param modelD_path: 人脸检测模型文件的路径。
        :param modelR_path: 人脸识别模型文件的路径。
        :param input_shape: 图像文件的统一尺寸
        """
        # 使用FaceDetector类检测图像中的人脸
        self.detector = FaceDetector(modelD_path, input_shape)
        self.recognizer = cv2.FaceRecognizerSF_create(model=modelR_path, config='')

    def recognize_face(self, image):
        """
        在给定的图像中识别人脸并返回有关识别出的人脸的信息。
        :param image: 要在其中识别人脸的图像。
        :return: 有关识别出的人脸的特征向量。
        """
        # 使用FaceDetector类检测图像中的人脸
        face_detect, image = self.detector.detector_image(image)
        if face_detect[1] is None:
            return None

        # 使用FaceRecognizer类提取人脸的特征向量
        face_align = self.recognizer.alignCrop(image, face_detect[1])
        face_feature = self.recognizer.feature(face_align)
        return face_feature

    def drawFace(self, IMG, faceArray):
        for face_index, face_coords in enumerate(faceArray[1]):
            thickness = 2

            # 准确度
            accuracy = face_coords[-1]

            # 坐标转成int类型
            coords = face_coords[:-1].astype(np.int32)

            # 框出人脸
            cv2.rectangle(IMG, (coords[0], coords[1]), (coords[0] + coords[2], coords[1] + coords[3]),
                          (0, 255, 0),
                          thickness)

            # 显示准确度
            cv2.putText(IMG, 'The accuracy of: {:.2f}'.format(accuracy), (1, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 1)
            return IMG
