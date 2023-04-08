import urllib
import urllib.request

import cv2
import numpy as np


class CameraIP:
    def __init__(self, url):
        """
        :param url:网络地址
        初始化CameraIP类的新实例
        """
        self.url = url

    def get_frame(self):
        """
        获取摄像头的当前帧。
        :return: 摄像头的当前帧。
        """
        imgResp = urllib.request.urlopen(self.url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        frame = cv2.imdecode(imgNp, -1)
        return  frame

