from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 100)
        self.slider.setSingleStep(1)
        self.slider.setPageStep(10)
        self.slider.valueChanged.connect(self.onValueChanged)

        vbox = QVBoxLayout()
        vbox.addWidget(self.slider)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('RGB Slider')
        self.show()

    def onValueChanged(self, value):
        # 计算对应的RGB值
        r = 255 if value > 50 else int(value * 5.1)
        g = int(value * 5.1) if value <= 50 else int((100 - value) * 5.1)
        b = 255 if value <= 50 else int((100 - value) * 5.1)

        # 将RGB值应用到LED上
        color = QColor(r, g, b)


if __name__ == '__main__':
    app = QApplication([])
    ex = Example()
    app.exec_()
