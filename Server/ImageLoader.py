import os
import cv2
import numpy as np


class ImageLoader:
    def __init__(self):
        """
        初始化ImageLoader类的新实例
        """
        self.images = []

    def load_image(self, path):
        """
        从文件中加载图像。
        :param path: 图像文件的路径。
        :return: 加载的图像。
        """
        image = cv2.imread(path)
        return image

    def load_folder_images(self, path):
        """
        获取文件夹中的图像
        :param path: 图像文件夹的路径
        :return: 文件夹中的图像列表
        """
        pic_file = os.listdir(path)
        for file_name in pic_file:
            pic_name = path + file_name
            img = cv2.imdecode(np.fromfile(pic_name, dtype=np.uint8), -1)
            self.images.append(img)

        if not self.images:
            raise Exception('No images found in folder')

        return self.images
