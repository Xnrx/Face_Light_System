import cv2

from IFaceDetector import IFaceDetector


class FaceDetector(IFaceDetector):
    def __init__(self, model_path, input_shape):
        """
        初始化FaceDetector类的新实例。
        :param model_path: 模型文件的路径。
        :param input_shape: 图像文件的统一尺寸
        """
        self.input_shape = input_shape
        self.detector = cv2.FaceDetectorYN_create(model=model_path, config='', input_size=input_shape)

    def detector_image(self, image):
        """
        在给定的图像中检测人脸并返回有关检测出的人脸的信息。
        :param image: 要在其中检测人脸的图像。
        :return: 有关检测出的人脸的信息与检测的图片。
        """
        image = cv2.resize(image, self.input_shape)
        face_detect = self.detector.detect(image)
        return face_detect, image
