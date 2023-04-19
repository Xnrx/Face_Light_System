from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QSlider, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.slider = QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.valueChanged.connect(self.updateColor)

        self.colorLabel = QLabel()
        self.colorLabel.setAutoFillBackground(True)

        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        layout.addWidget(self.colorLabel)
        self.setLayout(layout)

        self.updateColor(self.slider.value())

    def updateColor(self, value):
        # 将value映射到0-255的范围
        mapped_value = int(value / 100.0 * 255)

        # 根据value设置颜色
        if mapped_value <= 128:
            red = 2 * mapped_value
            green = 0
            blue = 255 - 2 * mapped_value
        else:
            red = 255 - 2 * (mapped_value - 128)
            green = 2 * (mapped_value - 128)
            blue = 0

        # 创建颜色对象并设置
        color = QColor(red, green, blue)

        color_rgb = tuple(int(color.name()[i:i + 2], 16) for i in (1, 3, 5))
        print(color_rgb)  # 输出结果为 (255, 0, 0)

        self.colorLabel.setStyleSheet("background-color: %s;" % color.name())

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
