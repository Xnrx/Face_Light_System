from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QColor, QStandardItem
from PyQt5.QtWidgets import QHeaderView, QTableView


class MyQStandardItemModelModel(QStandardItemModel):
    """
    重写QStandardItemModel的data函数，使QTableView全部item居中
    """

    def data(self, index, role=None):
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        return QStandardItemModel.data(self, index, role)


class Ui_select_all_user(QtWidgets.QWidget, QStandardItemModel):
    def setupUi(self, select_all_user, db):
        select_all_user.setObjectName("select_all_user")
        select_all_user.resize(520, 640)
        self._translate = QtCore.QCoreApplication.translate
        select_all_user.setWindowTitle(self._translate("select_all_user", "查看用户列表"))

        # 获取屏幕大小
        screen_size = QtWidgets.QDesktopWidget().screenGeometry(-1)
        screen_width, screen_height = screen_size.width(), screen_size.height()

        # 设置窗口大小
        window_width, window_height = 520, 640

        # 计算窗口左上角位置
        x = (screen_width - window_width) // 2 + 750
        y = (screen_height - window_height) // 2 - 50

        # 设置窗口位置和大小
        self.setGeometry(x, y, window_width, window_height)
        select_all_user.setMinimumSize(520, 640)
        select_all_user.setMaximumSize(520, 640)

        self.db = db

        # 创建网格布局
        self.gridLayout = QtWidgets.QGridLayout(select_all_user)
        self.gridLayout.setObjectName("gridLayout")

        # 设置表格样式
        self.tableWidget = QTableView(select_all_user)
        self.tableWidget.horizontalHeader().setStyleSheet("border:1px solid rgb(210, 210, 210);")
        self.tableWidget.horizontalHeader().resizeSection(0, 100)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 2)

        # 加载表格
        self.set_tables()

        # 设置退出按钮
        self.quit_button = QtWidgets.QPushButton(select_all_user)
        self.quit_button.setObjectName("quit_button")
        self.quit_button.setText("退出")
        self.quit_button.clicked.connect(select_all_user.close)
        self.gridLayout.addWidget(self.quit_button, 1, 1)

        QtCore.QMetaObject.connectSlotsByName(select_all_user)

    def set_tables(self):
        datas = self.db.query_all_user()

        len_row = len(datas)  # 获取数据长度
        self.model = MyQStandardItemModelModel(len_row, 6)
        self.tableWidget.setModel(self.model)

        # Set the text for the header items and the table items using a loop
        for i in range(5):
            item = QtGui.QStandardItem("Column " + str(i))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.model.setHorizontalHeaderItem(i, item)

        # 设置表头
        self.model.setHeaderData(0, Qt.Horizontal, "")
        self.model.setHeaderData(1, Qt.Horizontal, "序号")
        self.model.setHeaderData(2, Qt.Horizontal, "用户姓名")
        self.model.setHeaderData(3, Qt.Horizontal, "色温信息")
        self.model.setHeaderData(4, Qt.Horizontal, "亮度等级")
        self.model.setHeaderData(5, Qt.Horizontal, "参考颜色")
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)

        # 建立表格
        for i in range(len_row):
            for j in range(5):
                item = QtGui.QStandardItem()
                self.model.setItem(i, j, item)

        for index, row in enumerate(datas):
            name = row[0]
            rgb = f'{row[1]:03d},{row[2]:03d},{row[3]:03d}'
            Id = row[5]
            brightness = row[4]
            r = int(row[1])
            g = int(row[2])
            b = int(row[3])
            color = QColor(r, g, b)
            item_color = QStandardItem()
            item_color.setBackground(color)
            self.model.setData(self.model.index(index, 1), self._translate("select_all_user", str(Id)))
            self.model.setData(self.model.index(index, 2), self._translate("select_all_user", name))
            self.model.setData(self.model.index(index, 3), self._translate("select_all_user", rgb))
            self.model.setData(self.model.index(index, 4), self._translate("select_all_user", str(brightness)))
            self.model.setItem(index, 5, item_color)
