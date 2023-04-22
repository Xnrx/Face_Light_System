import sys

from PyQt5 import QtGui, QtWidgets

from AddWindow import AddWindowThread
from CameraThread import CameraThread
from DeleteWindow import DeleteWindowThread
from InitRecognizerSys import InitRecognizerSys
from QueryWindow import QueryWindowThread
from UI__MainWindow import Ui__MainWindow


class MainWindow(Ui__MainWindow, QtWidgets.QWidget):
    def __init__(self, parent=None):
        """
        初始化主窗口实例
        :param parent:
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.Sys = InitRecognizerSys()  # 所有窗口都用这个
        self.faceSys = self.Sys.faReSys
        self.db = self.Sys.db
        self.camera_thread = CameraThread(0, 'http://172.20.10.2/cam-hi.jpg', self.Sys)
        self.slot_init()

    def slot_init(self):
        """
        所有按钮信号槽初始化
        :return:
        """
        self.button_select_user.clicked.connect(self.button_query_user_clicked)
        self.button_close.clicked.connect(self.close)
        self.button_open_camera.clicked.connect(self.button_open_or_close_camera_clicked)
        self.button_add_user.clicked.connect(self.button_add_user_clicked)
        self.button_delete_user.clicked.connect(self.button_delete_user_clicked)
        self.button_add_user.setEnabled(False)

    # 添加窗口
    def button_add_user_clicked(self):
        """
        添加窗口按钮打开事件
        在添加窗口打开时关闭camera线程，关闭时打开camera线程，防止线程冲突
        :return:
        """
        # 暂时关闭线程
        self.camera_thread.stop()
        self.camera_thread.image_updated.disconnect(self.update_image_handle_com_and_buttons)  # 槽断开连接信号
        self.label_show_camera.clear()
        self.label_show_id.clear()
        self.button_open_camera.setText('打开摄像头')
        # 添加窗口线程打开
        self.add_thread = AddWindowThread(self.camera_thread.image, self.Sys)
        self.add_thread.add_window_closed.connect(self.on_add_window_closed)
        self.add_thread.start()

    def on_add_window_closed(self):
        """
        添加窗口按钮关闭事件
        :return:
        """
        # 打开线程
        self.camera_thread.image_updated.connect(self.update_image_handle_com_and_buttons)  # 槽连接信号
        self.camera_thread.is_running = True
        self.camera_thread.start()
        self.button_open_camera.setText('关闭摄像头')
        # 添加窗口线程关闭
        self.add_thread.quit()
        self.add_thread.wait()

    # 删除窗口
    def button_delete_user_clicked(self):
        """
        删除窗口按钮打开事件
        在添加窗口打开时关闭camera线程，关闭时打开camera线程，防止线程冲突
        :return:
        """
        # 添加窗口线程打开
        self.delete_thread = DeleteWindowThread(self.Sys, self.camera_thread.user.username)
        self.delete_thread.delete_window_closed.connect(self.on_delete_window_closed)
        self.delete_thread.start()

    def on_delete_window_closed(self):
        """
        添加窗口按钮关闭事件
        :return:
        """
        # 添加窗口线程关闭
        self.delete_thread.quit()
        self.delete_thread.wait()

    def button_query_user_clicked(self):
        """查询窗口按钮打开事件"""
        self.query_thread = QueryWindowThread(self.db)
        self.query_thread.is_running = True
        self.query_thread.query_window_closed.connect(self.on_query_window_closed)
        self.query_thread.start()

    def on_query_window_closed(self):
        """
        查询窗口按钮关闭事件
        :return:
        """
        self.query_thread.is_running = False
        self.query_thread.quit()
        self.query_thread.wait()

    def button_open_or_close_camera_clicked(self):
        """
        打开或关闭摄像头按钮事件
        :return:
        """
        if not self.camera_thread.is_running:
            self.camera_thread.image_updated.connect(self.update_image_handle_com_and_buttons)  # 槽连接信号
            self.camera_thread.is_running = True
            self.camera_thread.start()
            self.button_open_camera.setText('关闭摄像头')
        else:
            self.camera_thread.stop()
            self.camera_thread.image_updated.disconnect(self.update_image_handle_com_and_buttons)  # 槽断开连接信号
            self.label_show_camera.clear()
            self.label_show_id.clear()
            self.button_open_camera.setText('打开摄像头')

    def update_image_handle_com_and_buttons(self, image):
        """
        信号与槽-信号函数
        更新摄像头图像，显示图像id，向arduino发送信号，并处理按钮显示时机
        :param image:camera线程更新的图像
        :return:
        """
        self.label_show_camera.setPixmap(QtGui.QPixmap.fromImage(image))
        self.label_show_id.setText(self.camera_thread.user.username)

        # 添加按钮仅当有未登记人员时可用
        if self.camera_thread.user.username == '未登记人员':
            self.button_add_user.setEnabled(True)
        else:
            self.button_add_user.setEnabled(False)

        self.faceSys.receive_and_send_signal(self.camera_thread.user)

    def closeEvent(self, event):
        """
        主窗口关闭事件，断开串口通信
        :param event: 关闭事件
        :return:
        """
        # 执行一些代码
        self.faceSys.serial.close()
        self.faceSys.serial.open()
        self.faceSys.serial.close()
        # 调用父类的 closeEvent 方法
        super(MainWindow, self).closeEvent(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 固定的，表示程序应用
    ui = MainWindow()  # 实例化Ui_MainWindow
    ui.show()  # 调用ui的show()以显示。同样show()是源于父类QtWidgets.QWidget的
    sys.exit(app.exec_())  # 不加这句，程序界面会一闪而过

