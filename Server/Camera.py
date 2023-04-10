import cv2


class Camera:
    def __init__(self, camera_index=0):
        """
        初始化Camera类的新实例。
        :param camera_index: 摄像头的索引。
        """
        self.camera_index = camera_index
        self.capture = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    def get_frame(self):
        """
        获取摄像头的当前帧。
        :return: 摄像头的当前帧。
        """
        ret, frame = self.capture.read()
        if ret:
            return frame
        else:
            return None

    def release(self):
        """
        释放摄像头。
        """
        self.capture.release()
