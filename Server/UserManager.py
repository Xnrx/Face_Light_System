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
        new_user_id = self.add_user()
        new_user = self.add_user_images(image, new_user_id)
        new_user.load_user_features(modelD_path, modelR_path, input_shape)
        self.list.append(new_user)

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

    def load_rgbs(self, datas):
        """
        加载用户rgb信息
        :param datas:数据库数据集
        """
        # 根据信息设计字典
        for row in datas:
            name = row[0]
            rgb = f'{row[1]:03d}{row[2]:03d}{row[3]:03d}'
            self.rgb_dic[name] = rgb
        print(self.rgb_dic)
        for user in self.list:
            user.RGB = self.rgb_dic.get(user.user_id, '000000000')
