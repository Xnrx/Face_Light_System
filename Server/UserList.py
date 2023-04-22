import datetime
import os

import cv2

from User import User


class UserList:
    def __init__(self, path, list):
        """
        初始化UserList类的实例
        :param path: 用户路径
        :param list: 用户列表
        """
        self.path = path
        self.list = list
        self.rgb_dic = {}

    def load(self):
        """
        加载用户列表
        """
        pic_file = os.listdir(self.path)
        for file_name in pic_file:
            self.list.append(User(str(file_name)))

    def add_user(self):
        """
        添加新用户
        :return: 新用户id
        """
        user_id = input("请输入姓名:")
        path = f'../user/{user_id}/images/'
        if not os.path.exists(path):
            os.makedirs(path)
        return user_id

    def add_user_images(self, image, user_id):
        """
        添加用户
        :param user_id: 要添加的用户的id
        :param image: 要添加的用户的照片
        :return: 新用户
        """

        # 添加新用户
        file_name = None
        len_path = self.get_user_images_len(user_id)
        now = datetime.datetime.now()
        current_time = now.strftime("%Y%m%d%H%M%S")
        if len_path >= 5:
            print("您的照片已超过五张，无法录入")
        else:
            file_name = current_time
            new_path = f"../user/{user_id}/images/{file_name}.jpg"
            cv2.imencode('.jpg', image)[1].tofile(new_path)
            print("已录入人脸")

        return User(user_id, file_name=file_name)

    def get_user_images_len(self, user_id):
        """
        查看用户图像个数
        :param user_id: 要查看的用户的id
        :return: 该用户图像数量
        """
        path = f'../user/{user_id}/images/'
        pic_file = os.listdir(path)
        len_path = len(pic_file)
        return len_path
