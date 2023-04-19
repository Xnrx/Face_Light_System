import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QWidget

from AddUI import Ui_Add_User_Dialog


class AddWindow(QDialog, Ui_Add_User_Dialog):
    def __init__(self, Sys, img):
        super().__init__()
        self.setupUi(self, Sys, img)

    def closeEvent(self, event):
        if event.isAccepted():
            # 执行你想要的代码
            print("关闭事件被接受")
        event.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 固定的，表示程序应用
    ui = AddWindow()  # 实例化Ui_MainWindow
    ui.show()  # 调用ui的show()以显示。同样show()是源于父类QtWidgets.QWidget的
    sys.exit(app.exec_())  # 不加这句，程序界面会一闪而过
