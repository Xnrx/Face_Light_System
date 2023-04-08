import pymssql

class Database:
    def __init__(self, server, user, password, database):
        """
        初始化DataBase实例
        :param server: 服务器
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名称
        """
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None


    def connect(self):
        """
        连接数据库
        :return:
        """
        # 建立数据库连接
        self.conn = pymssql.connect(server=self.server, user=self.user, password=self.password, database=self.database, charset='GB18030')
        # 获取游标
        self.cursor = self.conn.cursor()

    def query(self, sql, params=None):
        """
        查询数据库
        :param sql:查询语句
        :param params: 可选参数
        :return: 结果集
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def close(self):
        """
        关闭数据库连接
        """
        self.cursor.close()
        self.conn.close()