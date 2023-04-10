from Camera import Camera
from CameraIP import CameraIP


class CameraSelector:
    def __init__(self, camera_type='local', camera_index=0, url=None):
        """
        初始化CameraSelector类的新实例。
        :param camera_type: 摄像头类型，可以是'local'或'ip'。
        :param camera_index: 摄像头的索引（仅适用于本地摄像头）。
        :param url: 摄像头的URL（仅适用于IP摄像头）。
        """
        self.camera_type = camera_type
        self.camera_index = camera_index
        self.url = url
        if camera_type == 'local':
            self.camera = Camera(self.camera_index)
        elif camera_type == 'ip':
            self.camera = CameraIP(self.url)

    def set_camera(self, camera_type):
        """
        设置摄像头类型
        :param camera_type: 摄像头类型，可以是'local'或'ip'。
        """
        self.camera_type = camera_type
        if camera_type == 'local':
            self.camera = Camera(self.camera_index)
        elif camera_type == 'ip':
            self.camera = CameraIP(self.url)

    def get_camera_type(self):
        """
        返回摄像头类型
        :return: 摄像头类型
        """
        return self.camera_type
