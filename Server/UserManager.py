import os
import shutil

from UserList import UserList


class UserManager(UserList):
    def __init__(self, path, list):
        """
        初始化UserManager类的实例
        :param path: 用户路径
        :param list: 用户列表
        """
        UserList.__init__(self, path, list)

    def add_new_user(self, image, modelD_path, modelR_path, input_shape):
        """
        添加新用户
        :param input_shape: 图像格式
        :param modelR_path: 人脸识别模型
        :param modelD_path: 人脸检测模型
        :param image: 新用户照片
        :return: 新用户
        """
        new_user_name = self.add_user()
        new_user = self.add_user_images(image, new_user_name)
        new_user.load_user_features(modelD_path, modelR_path, input_shape)
        self.list.append(new_user)

    def add_new_user_Client(self, image, user_name, modelD_path, modelR_path, input_shape):
        """
        添加新用户
        :param user_name: 用户id
        :param input_shape: 图像格式
        :param modelR_path: 人脸识别模型
        :param modelD_path: 人脸检测模型
        :param image: 新用户照片
        :return: 新用户
        """
        new_user_name = user_name
        path = f'../user/{user_name}/images/'
        if not os.path.exists(path):
            os.makedirs(path)
        new_user = self.add_user_images(image, new_user_name)
        if new_user.file_name is not None:
            new_user.add_user_features(modelD_path, modelR_path, input_shape)
        self.list.append(new_user)

    def remove_user_Client(self, user_name):
        """
        添加新用户
        :param user_name: 用户id
        """
        path = f'../user/{user_name}/'
        if os.path.exists(path):
            shutil.rmtree(path)

        matched_users = [user for user in self.list if user.username == user_name]

        if matched_users:
            # 找到了匹配的 User 对象
            matched_user = matched_users[0]
        else:
            # 没有找到匹配的 User 对象
            matched_user = None

        self.list.remove(matched_user)

    def load_images_and_features(self, modelD_path, modelR_path, input_shape):
        """
        加载用户照片与特征向量
        :param input_shape: 图像格式
        :param modelR_path: 人脸识别模型
        :param modelD_path: 人脸检测模型
        """
        self.load()
        for user in self.list:
            user.load_user_features(modelD_path, modelR_path, input_shape)

    def load_rgbs_brightness(self, datas):
        """
        加载用户rgb信息和亮度信息
        :param datas:数据库数据集
        """
        # 根据信息设计字典
        bright = 0
        for row in datas:
            row = list(row)
            name = row[0]
            bright = row[4]
            row[1] = int(row[1] * bright / 5)
            row[2] = int(row[2] * bright / 5)
            row[3] = int(row[3] * bright / 5)
            rgb = f'{row[1]:03d}{row[2]:03d}{row[3]:03d}'
            self.rgb_dic[name] = rgb

        print(self.rgb_dic)
        for user in self.list:
            user.RGB = self.rgb_dic.get(user.username, '000000000')
            if bright == 0:
                exit("亮度信息错误")
            user.brightness = bright
