from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QColor, QStandardItem
from PyQt5.QtWidgets import QHeaderView, QTableView, QFrame

from Database import Database


class MyQStandardItemModelModel(QStandardItemModel):
    """
    重写QStandardItemModel的data函数，使QTableView全部item居中
    """
    def data(self, index, role=None):
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return QStandardItemModel.data(self, index, role)


class Ui_select_all_user(QtWidgets.QWidget, QStandardItemModel):
    def setupUi(self, select_all_user):
        select_all_user.setObjectName("select_all_user")
        select_all_user.resize(520, 640)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(select_all_user)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # 设置表格样式
        self.tableWidget = QTableView(select_all_user)
        self.tableWidget.horizontalHeader().setStyleSheet("border:1px solid rgb(210, 210, 210);")
        self.tableWidget.horizontalHeader().resizeSection(0, 100)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.horizontalLayout_2.addWidget(self.tableWidget)

        # 连接数据库
        self.db = Database(server='LAPTOP-NO19G1TG', user='sa', password='zhong5567', database='Python')  # 数据库初始化
        self.db.connect()

        # 加载表格
        self.set_tables(select_all_user)

        self.quit_button = QtWidgets.QPushButton(select_all_user)
        self.quit_button.setObjectName("quit_button")
        self.quit_button.setText("退出")
        self.quit_button.clicked.connect(select_all_user.close)
        self.horizontalLayout_2.addWidget(self.quit_button)

        QtCore.QMetaObject.connectSlotsByName(select_all_user)

    def set_tables(self, select_all_user):

        datas = self.db.query('SELECT * FROM UserSettings')
        _translate = QtCore.QCoreApplication.translate
        select_all_user.setWindowTitle(_translate("select_all_user", "查看用户列表"))

        len_row = len(datas)
        self.model = MyQStandardItemModelModel(len_row, 5)
        self.tableWidget.setModel(self.model)

        # Set the text for the header items and the table items using a loop
        for i in range(5):
            item = QtGui.QStandardItem("Column " + str(i))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.model.setHorizontalHeaderItem(i, item)

        self.model.setHeaderData(0, Qt.Horizontal, "")
        self.model.setHeaderData(1, Qt.Horizontal, "序号")
        self.model.setHeaderData(2, Qt.Horizontal, "用户姓名")
        self.model.setHeaderData(3, Qt.Horizontal, "用户灯色")
        self.model.setHeaderData(4, Qt.Horizontal, "")

        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

        for i in range(len_row):
            for j in range(4):
                item = QtGui.QStandardItem()
                self.model.setItem(i, j, item)

        for index, row in enumerate(datas):
            name = row[0]
            rgb = f'{row[1]:03d},{row[2]:03d},{row[3]:03d}'
            Id = row[4]
            r = int(row[1])
            g = int(row[2])
            b = int(row[3])
            color = QColor(r, g, b)
            item_color = QStandardItem()
            item_color.setBackground(color)
            self.model.setData(self.model.index(index, 1), _translate("select_all_user", str(Id)))
            self.model.setData(self.model.index(index, 2), _translate("select_all_user", name))
            self.model.setData(self.model.index(index, 3), _translate("select_all_user", rgb))
            self.model.setItem(index, 4, item_color)


