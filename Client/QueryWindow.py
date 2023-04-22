import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QDialog

from Database import Database
from queryUI import Ui_select_all_user


class QueryWindowThread(QThread):
    # 槽
    query_window_closed = pyqtSignal()

    def __init__(self, db):
        """
        初始化查询窗口实例
        :param db: 数据库系统
        """
        super(QueryWindowThread, self).__init__()
        self.query_window = QueryWindow(db)  # 初始化窗口ui
        self.query_window.exec_()
        self.is_running = False

    def run(self):
        """
        线程执行函数
        :return:
        """
        self.query_window_closed.emit()


class QueryWindow(QDialog, Ui_select_all_user):
    def __init__(self, db):
        super(Ui_select_all_user, self).__init__()
        # 连接数据库
        self.db = db
        self.setupUi(self, self.db)

    def closeEvent(self, event):
        QtWidgets.QApplication.processEvents(QtCore.QEventLoop.AllEvents, 100)  # 处理所有未处理的事件
        event.accept()  # 关闭子窗口


if __name__ == '__main__':
    db = Database(server='LAPTOP-NO19G1TG', user='sa', password='zhong5567', database='Python')  # 数据库初始化
    db.connect()
    app = QtWidgets.QApplication(sys.argv)  # 固定的，表示程序应用
    ui = QueryWindow()  # 实例化Ui_MainWindow
    ui.show()  # 调用ui的show()以显示。同样show()是源于父类QtWidgets.QWidget的
    sys.exit(app.exec_())  # 不加这句，程序界面会一闪而过
