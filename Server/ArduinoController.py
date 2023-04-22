import serial

from IArduinoController import IArduinoController


class ArduinoController(IArduinoController):
    def __init__(self, port, Rate):
        """
        初始化ArduinoController类的新实例。
        :param port: Arduino板所连接的串行端口。
        """
        self.serial = serial.Serial(port, Rate)

    def send_signal(self, signal):
        """
        向Arduino板发送信号,并清除缓冲区。
        :param signal: 要发送的信号。
        """
        self.serial.write(signal.encode())
        self.serial.flush()

    def receive_signal(self, encode):
        """
        接收Arduino板发来的信号,忽略译码失败的信号。
        :param encode: 译码格式。
        :return val: 信号
        """
        try:
            val = self.serial.readline().decode(encode).strip()
            print(val)
        except UnicodeDecodeError:
            self.serial.readline().decode(encode, errors='ignore')
            val = 'ignore'
        return val
